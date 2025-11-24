# University Project Presentation Website

A professional, dark-mode website designed for presenting academic research projects with data visualization and analysis.

## Features

- **Dark Mode Only**: Professional dark theme with modern design
- **Responsive Layout**: Works on desktop and mobile devices
- **Interactive Tabs**: Switch between Overview, Raw Data, and Cleaned Data views
- **Data Visualization**: Display large datasets (2000+ rows) with pagination
- **Search Functionality**: Filter data in real-time
- **Metrics Dashboard**: Key statistics and data quality indicators
- **Smooth Animations**: Professional transitions and hover effects

## Project Structure

```
project/
├── index.html          # Main HTML file
├── styles.css          # Dark mode styling
├── script.js           # Interactive functionality and data generation
└── README.md          # This file
```

## How to Use

1. **Open the Website**: Simply open `index.html` in any modern web browser (Chrome, Firefox, Edge, Safari)

2. **Navigate Sections**:
   - **Overview**: View key metrics and project summary
   - **Raw Data**: Browse the original dataset with missing values and duplicates
   - **Cleaned Data**: View the processed dataset with 100% quality

3. **Interact with Data**:
   - Use the search bar to filter data
   - Change the number of rows displayed (50/100/200)
   - Navigate through pages using Previous/Next buttons

## Customization Guide

### Change Project Title

Edit line 13 in `index.html`:
```html
<h1 class="project-title">YOUR TITLE HERE</h1>
```

### Modify Color Scheme

Edit the CSS variables in `styles.css` (lines 10-22):
```css
:root {
    --bg-primary: #0a0e17;        /* Main background */
    --accent-primary: #3b82f6;    /* Primary accent color */
    --accent-secondary: #8b5cf6;  /* Secondary accent color */
    /* ... other colors ... */
}
```

### Use Your Own Data

Replace the data generation functions in `script.js`:

1. **For Raw Data** - Replace the `generateRawData()` function with your actual data:
```javascript
let rawData = [
    { id: 1, name: 'Item 1', category: 'Cat A', value: 100, date: '2024-01-01', status: 'Active' },
    { id: 2, name: 'Item 2', category: 'Cat B', value: 200, date: '2024-01-02', status: 'Pending' },
    // ... your data here
];
```

2. **For Cleaned Data** - Either use the `generateCleanedData()` function or provide your own:
```javascript
let cleanedData = [
    { id: 1, name: 'Item 1', category: 'Cat A', value: 100, date: '2024-01-01', status: 'Active' },
    // ... your cleaned data here
];
```

### Load Data from CSV/JSON

Add this function to `script.js` to load external data:

```javascript
// For JSON files
async function loadJSONData(url) {
    const response = await fetch(url);
    return await response.json();
}

// Then use it:
// let rawData = await loadJSONData('raw-data.json');
```

### Modify Table Columns

1. Edit the table headers in `index.html` (lines 71-79 for raw data, similar for cleaned data)
2. Update the row rendering in `script.js` (line 151 in the `renderTable` function)

### Change Metrics

Edit the metrics cards in `index.html` (lines 31-56) and update calculations in `script.js` (lines 108-125)

## Tips for Presentation

1. **Preparation**: Test all features before presenting
2. **Navigation**: Use tab navigation to show data transformation process
3. **Search Demo**: Demonstrate the search functionality with relevant terms
4. **Metrics**: Highlight the data quality improvement from raw to cleaned data
5. **Pagination**: Show how you can browse through large datasets efficiently

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Internet Explorer: Not supported

## Technical Details

- Pure HTML/CSS/JavaScript (no external dependencies)
- Client-side data generation and filtering
- Responsive design with mobile support
- Optimized for performance with large datasets

## Troubleshooting

**Website not loading?**
- Ensure all three files (index.html, styles.css, script.js) are in the same folder
- Try opening in a different browser

**Data not showing?**
- Check browser console for errors (F12)
- Ensure JavaScript is enabled in your browser

**Styling issues?**
- Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Ensure styles.css is in the same directory as index.html

## Future Enhancements

- Export data to CSV/Excel
- Add data visualization charts
- Multiple dataset support
- Print-friendly view
- Dark/Light mode toggle (currently dark mode only)

---

**Created for Academic Presentation Purposes**
