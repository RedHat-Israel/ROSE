import { loadTemplate, loadStylesheet } from './componentUtils.js';

const [innerHTML, sheet] = await Promise.all([
    loadTemplate('./settings-form.html'),
    loadStylesheet('./settings-form.css')
]);

class SettingsForm extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.shadowRoot.innerHTML = innerHTML;
        this.shadowRoot.adoptedStyleSheets = [sheet];
        
        this.loadDrivers();
        this.shadowRoot.querySelector('#submit-button').addEventListener('click', this.sendDrivers.bind(this));
        this.shadowRoot.querySelector('#cancel-button').addEventListener('click', this.cancelSetting.bind(this));
    }

    displayError(message) {
        const errorMessageElement = this.shadowRoot.getElementById('error-message');
        errorMessageElement.textContent = message;
    }

    async loadDrivers() {
        try {
            const response = await fetch('/admin', { method: 'POST' });
            const data = await response.json();

            if (data.drivers && data.drivers.length > 0) {
                this.shadowRoot.getElementById('driver1').value = data.drivers[0] ?? "";
                this.shadowRoot.getElementById('driver2').value = data.drivers[1] ?? "";
            }
        } catch (error) {
            this.displayError('Error loading drivers: ' + error.message);
        }
    }

    async sendDrivers(event) {
        event.preventDefault();

        const driver1 = this.shadowRoot.getElementById('driver1').value;
        const driver2 = this.shadowRoot.getElementById('driver2').value;

        const params = new URLSearchParams();
        params.append('drivers', `${driver1},${driver2}`);

        try {
            const response = await fetch(`/admin?${params}`, { method: 'POST' });

            if (response.ok) {
                window.location.href = "/index.html";
            } else {
                this.displayError('Error sending drivers: ' + response.statusText);
            }
        } catch (error) {
            this.displayError('Error sending drivers: ' + error.message);
        }   
    }

    cancelSetting(event) {
        event.preventDefault();
        window.location.href = "/index.html";
    }
}

customElements.define('settings-form', SettingsForm);
