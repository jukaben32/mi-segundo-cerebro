const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://micheline-nail-bar.vercel.app/#booking');
  
  // Wait for the form to be visible
  await page.waitForSelector('form');
  
  // Get the form HTML
  const formHtml = await page.evaluate(() => {
    const form = document.querySelector('form');
    return form ? form.outerHTML : 'Form not found';
  });
  
  fs.writeFileSync('v1_form.html', formHtml);
  
  // Also get some CSS variables or styles for colors
  const styles = await page.evaluate(() => {
    const root = document.documentElement;
    const styles = getComputedStyle(root);
    return {
      primary: styles.getPropertyValue('--primary') || 'not found',
      secondary: styles.getPropertyValue('--secondary') || 'not found',
      accent: styles.getPropertyValue('--accent') || 'not found',
      bg: styles.getPropertyValue('--background') || 'not found',
      text: styles.getPropertyValue('--foreground') || 'not found'
    };
  });
  
  fs.writeFileSync('v1_styles.json', JSON.stringify(styles, null, 2));
  
  await browser.close();
})();
