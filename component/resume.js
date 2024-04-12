// declare a custom element
customElements.define("professional-resume", class extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({mode: "open"});

        const data = this.getAttribute("data");
        const dataUrl = this.getAttribute("data-url");
        const {
            name
        } = JSON.parse(data || "{}");
        
        fetch("component/resume.html")
            .then(response => response.text())
            .then(html => {
                let parser = new DOMParser();
                let resumeDoc = parser.parseFromString(html, "text/html");
                let resumeTemplate = resumeDoc.querySelector("template");
                this.shadowRoot.appendChild(resumeTemplate.content.cloneNode(true));

                if (dataUrl) {
                    fetch(dataUrl)
                        .then(response => response.json())
                        .then(data => {
                            const {
                                name,
                                contact,
                                experience,
                                education
                            } = data;
                            this.shadowRoot.querySelector("#name").textContent = name;
                            // set #email, #phone, #address from contact
                            this.shadowRoot.querySelector("#email").textContent = contact.email;
                            this.shadowRoot.querySelector("#phone").textContent = contact.phone;
                            this.shadowRoot.querySelector("#address").textContent = contact.address;
                        });
                }

                this.shadowRoot.querySelector("#name").textContent = name;

                // fetch the styles
                fetch("component/resume.css")
                    .then(response => response.text())
                    .then(css => {
                        let style = document.createElement("style");
                        style.textContent = css;
                        this.shadowRoot.appendChild(style);
                    });
            });
    }
});