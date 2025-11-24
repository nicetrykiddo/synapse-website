# Circuits Folder

Place your Logisim circuit file (`cao.circ`) here for download functionality in the CAO section.

## File to Add

- `cao.circ` - Your Logisim circuit file

## How to Use Your Circuit on the Website

### Option 1: Interactive Simulator (Recommended)

1. **Upload to CircuitVerse:**
   - Go to https://circuitverse.org/
   - Create a free account
   - Click "Create New Project"
   - Import your `.circ` file OR design in their web editor
   - Save and set project to **Public**

2. **Get Embed URL:**
   - Open your project
   - Click "Share" button
   - Copy the **Embed URL**

3. **Update Website:**
   - Open `index.html`
   - Find line 302 (the iframe element)
   - Replace the `src` URL with your embed URL:
   ```html
   <iframe
       id="logisim-frame"
       src="https://circuitverse.org/simulator/embed/YOUR-PROJECT-ID"
       class="circuit-iframe"
       frameborder="0"
       allowfullscreen>
   </iframe>
   ```

### Option 2: Download Only

If you only want to provide a download link:

1. Place your `cao.circ` file in this folder
2. The download button is already configured in the HTML
3. Users can download and open in Logisim Evolution locally

## About Logisim

**Logisim Evolution** is a digital logic design and simulation tool.

- **Download:** https://github.com/logisim-evolution/logisim-evolution/releases
- **Documentation:** https://github.com/logisim-evolution/logisim-evolution/wiki

## CircuitVerse Benefits

- **No installation required** - Runs in browser
- **Interactive simulation** - Users can interact with your circuit
- **Shareable** - Easy to embed in websites
- **Free** - Completely free to use
- **Compatible** - Can import Logisim files

## Tips for Better Circuit Presentations

1. **Add Labels:** Clearly label all inputs, outputs, and major components
2. **Use Colors:** Different colors for different parts of the circuit
3. **Add Text:** Include descriptions or notes in the circuit
4. **Organize Layout:** Keep wires neat and components aligned
5. **Test Thoroughly:** Make sure the circuit works before uploading

## Circuit File Structure

```
circuits/
├── cao.circ          # Your Logisim circuit file
└── README.md        # This file
```

## Example Circuits to Create

For a Computer Architecture course, consider:
- ALU (Arithmetic Logic Unit)
- Register files
- Memory units
- CPU components
- Control units
- Simple processors

---

**After setting up CircuitVerse, your circuit will be fully interactive on the website!**
