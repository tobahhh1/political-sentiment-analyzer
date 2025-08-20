fetch("/static/components/button/button.html")
    .then(stream => stream.text())
    .then(text => define(text));

function define(html) {
    class Button extends HTMLElement {
        constructor() {
            super();
            var shadow = this.attachShadow({ mode: 'open' });
            shadow.innerHTML = html;
        }
    }

    customElements.define('tobahhh1-psa-button', Button);
}
