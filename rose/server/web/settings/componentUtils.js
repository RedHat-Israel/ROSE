export async function loadTemplate(path) {
    try {
        const response = await fetch(path);
        return await response.text();
    } catch (error) {
        console.error('Error loading template:', error);
    }
}

export async function loadStylesheet(path) {
    try {
        const response = await fetch(path);
        const cssText = await response.text();

        const sheet = new CSSStyleSheet();
        sheet.replaceSync(cssText);

        return sheet;
    } catch (error) {
        console.error('Error loading stylesheet:', error);
    }
}
