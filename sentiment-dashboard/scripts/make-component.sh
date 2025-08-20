#!/bin/bash

COMPONENT_EL_NAME="${1}"
PREFIX_NAME=tobahhh1-psa
COMPONENT_CLASS_NAME=$(echo "${1}" | sed -E 's/(^|-)(\w)/\U\2/g')
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR/../src/static/components
mkdir $COMPONENT_EL_NAME
cd $COMPONENT_EL_NAME

cat << EOF > "${COMPONENT_EL_NAME}.html"
<link rel="stylesheet" href="/static/${COMPONENT_EL_NAME}/${COMPONENT_EL_NAME}.css">
EOF

cat << EOF > "${COMPONENT_EL_NAME}.js"
fetch("/static/components/${COMPONENT_EL_NAME}/${COMPONENT_EL_NAME}.html")
    .then(stream => stream.text())
    .then(text => define(text));

function define(html) {
    class ${COMPONENT_CLASS_NAME} extends HTMLElement {
        constructor() {
            super();
            var shadow = this.attachShadow({mode: 'open'});
            shadow.innerHTML = html;
        }
    }

    customElements.define('${PREFIX_NAME}-${COMPONENT_EL_NAME}', ${COMPONENT_CLASS_NAME});
}
EOF

touch "${COMPONENT_EL_NAME}.css"
