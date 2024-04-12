// declare a custom element
customElements.define("professional-resume", class extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({mode: "open"});
        console.log("Professional Resume Created");
        
        // read the template from the fs
        fetch("component/resume.html")
            .then(response => response.text())
            .then(html => {
                let parser = new DOMParser();
                let resumeDoc = parser.parseFromString(html, "text/html");
                let resumeTemplate = resumeDoc.querySelector("template");
                this.template = resumeTemplate;
                this.shadowRoot.appendChild(this.template.content.cloneNode(true));
            });
        // create a shadow root
    }
});