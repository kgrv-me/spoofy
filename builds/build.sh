#!/bin/sh

LOCAL_CMD="debug release"
LOCAL=false
RELEASE_CMD="release"
RELEASE=false
WORK_PATH=$(echo "$(pwd)/$(dirname ${0})/..")
ZIP=false

# WORKDIR to parent of script directory
echo "  ~ PWD: $(pwd)"
cd "${WORK_PATH}"

# Set 'LOCAL' if empty or applicable
if [ -z "${1}" ] || (echo "${LOCAL_CMD}" | grep -w "${1}" > /dev/null); then
    LOCAL=true
fi

# Set 'RELEASE' if applicable
(echo "${RELEASE_CMD}" | grep -w "${1}" > /dev/null) && RELEASE=true

# Set 'ZIP' if applicable
([ "${RELEASE}" = true ] || [ "${1}" = 'zip' ]) && ZIP=true

# Set expected GitHub runner environment variables for local
if [ "${LOCAL}" = true ]; then
    ARCH='ARM64'
    RUNNER_OS='macOS'
fi

# Display configurations
echo "  ~ CMD: ${1}"
echo "  ~ LOCAL: ${LOCAL}"
echo "  ~ RELEASE: ${RELEASE}"
echo "  ~ ZIP: ${ZIP}"
echo "  ~ ARCH: ${ARCH}"
echo "  ~ RUNNER_OS: ${RUNNER_OS}"

# Generate API documentation using 'pdoc3'
if [ "${1}" = 'docs' ] || [ "${RELEASE}" = true ]; then
    pip3 install --upgrade pdoc3
    pdoc3 --close-stdin --force --html --output-dir docs spoofy
    mv docs/spoofy/* docs/.
    rm -rf docs/spoofy
    [ "${1}" = 'docs' ] && exit 0
fi

# Create INFO file if applicable
if [ "${1}" = 'info' ] || [ "${LOCAL}" = true ]; then
    if [ -n "${2}" ]; then
        printf '{"ARCH": "'"${ARCH}"'", "OS": "'"${RUNNER_OS}"'", "VERSION": "'"${2}"'"}' > spoofy/INFO
        echo "  ~ INFO: $(cat spoofy/INFO)"
        [ "${1}" = 'info' ] && exit 0
    elif [ -z "${2}" ]; then
        echo "  ~ [e] Missing 2nd positional argument 'TAG'"
        exit 22
    fi
fi

EXE_NAME="Spoofy-${RUNNER_OS}-${ARCH}"

# Configure PyOxidizer BZL
if [ "${1}" = 'config' ] || [ "${LOCAL}" = true ]; then
    echo "  ~ Configure PyOxidizer BZL"

    LIB_PATH=$(pip3 show scapy | grep Location | cut -d ' ' -f2 | sed 's/\\/\\\\\\\\/g')
    PYOX_BZL="pyoxidizer.bzl"
    SED_0="s/SPOOFY/Spoofy-${RUNNER_OS}-${ARCH}/"
    SED_1="s|venv/lib/python3.10/site-packages|${LIB_PATH}|"

    echo "  ~ LIB_PATH: ${LIB_PATH}"
    echo "  ~ PYOX_BZL: ${PYOX_BZL}"
    echo "  ~ SED_0: ${SED_0}"
    echo "  ~ SED_1: ${SED_1}"

    cp ./builds/pyoxidizer.bzl .
    if [ "${RUNNER_OS}" = 'macOS' ]; then
        sed -i '' "${SED_0}" ${PYOX_BZL}
        [ "${LOCAL}" = false ] && sed -i '' "${SED_1}" ${PYOX_BZL}
    else
        sed -i "${SED_0}" ${PYOX_BZL}
        [ "${LOCAL}" = false ] && sed -i "${SED_1}" ${PYOX_BZL}
    fi
    [ "${1}" = 'config' ] && exit 0
fi

# Build standalone
if [ "${RELEASE}" = true ] || [ "${LOCAL}" = true ]; then
    # Install dependencies
    pip3 install --requirement builds/requirements.txt

    # Remove previous artifacts
    echo "  ~ Removing previous build artifacts..."
    rm "${EXE_NAME}.zip"
    rm -rf build

    # Patch then build
    echo "  ~ Apply Patch"
    ./builds/patch.py refresh-packages
    echo "  ~ Building Standalone..."
    if [ "${RELEASE}" = true ]; then
        pyoxidizer build --release
    elif [ "${LOCAL}" = true ]; then
        pyoxidizer run
    fi
fi

# Zip standalone
if [ "${ZIP}" = true ]; then
    EXE_PATH=$(find . -name "${EXE_NAME}*")
    DIR_PATH=$(dirname ${EXE_PATH})

    echo "  ~ EXE_NAME: ${EXE_NAME}"
    echo "  ~ EXE_PATH: ${EXE_PATH}"
    echo "  ~ DIR_PATH: ${DIR_PATH}"
    echo "  ~ WORK_PATH: ${WORK_PATH}"

    # Add extra files
    cp LICENSE README.md ${DIR_PATH}/.
    cd ${DIR_PATH}
    if [ "${RUNNER_OS}" != 'Windows' ]; then
        echo "  ~ Creating 'run.sh' for 'macOS' and 'Linux'..."
        echo '#!/bin/sh\nexec sudo "$(dirname $0)/'"${EXE_NAME}"'"' > run.sh
        chmod 555 run.sh $(basename ${EXE_PATH})
    fi

    echo "  ~ List Contents"
    ls -l

    cd ..
    echo "  ~ Zipping Standalone..."
    if [ "${RUNNER_OS}" = 'Windows' ]; then
        pwsh -Command "Compress-Archive -Path Spoofy -DestinationPath ${EXE_NAME}.zip"
    else
        zip -r ${EXE_NAME}.zip Spoofy
    fi

    # Move .zip to WORKDIR if applicable
    mv ${EXE_NAME}.zip ${WORK_PATH}/.
fi

# Cleanup
echo "  ~ Cleaning up..."
cd "${WORK_PATH}" && rm pyoxidizer.bzl spoofy/INFO