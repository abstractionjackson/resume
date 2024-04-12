// declare a custom element
customElements.define("professional-resume", class extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({mode: "open"});
        
        fetch("component/resume.html")
            .then(response => response.text())
            .then(html => {
                let parser = new DOMParser();
                let resumeDoc = parser.parseFromString(html, "text/html");
                let resumeTemplate = resumeDoc.querySelector("template");
                this.shadowRoot.appendChild(resumeTemplate.content.cloneNode(true));
            });
    }
});