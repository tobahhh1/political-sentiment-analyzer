fetch("/static/components/navbar/navbar.html")
    .then(stream => stream.text())
    .then(text => define(text));

function define(html) {
    class Navbar extends HTMLElement {
        constructor() {
            super();
            var shadow = this.attachShadow({ mode: 'open' });
            shadow.innerHTML = html;


        }
    }

    customElements.define('tobahhh1-psa-navbar', Navbar);
}
