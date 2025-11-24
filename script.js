// ========================================
// DATA MANAGEMENT SYSTEM
// ========================================

// Available datasets
const DATASETS = {
    field: {
        name: 'Field Reports',
        icon: 'fa-flag',
        rawPath: 'data/raw/field.csv',
        cleanedPath: 'data/cleaned/cleaned_field.csv',
        description: 'Field failure and incident reports'
    },
    manufacturing: {
        name: 'Manufacturing Data',
        icon: 'fa-industry',
        rawPath: 'data/raw/manufacturing.csv',
        cleanedPath: 'data/cleaned/cleaned_manufacturing.csv',
        description: 'Manufacturing process and quality data'
    },
    sales: {
        name: 'Sales Data',
        icon: 'fa-shopping-cart',
        rawPath: 'data/raw/sales.csv',
        cleanedPath: 'data/cleaned/cleaned_sales.csv',
        description: 'Sales transactions and customer data'
    },
    testing: {
        name: 'Testing Data',
        icon: 'fa-flask',
        rawPath: 'data/raw/testing.csv',
        cleanedPath: 'data/cleaned/cleaned_testing.csv',
        description: 'Product testing and quality assurance data'
    }
};

// Current state
let currentDataset = 'field';
let rawData = [];
let cleanedData = [];
let dataStats = {
    raw: { total: 0, missing: 0, nulls: 0 },
    cleaned: { total: 0, missing: 0, nulls: 0 },
    quality: 0
};

// Parse CSV data
function parseCSV(text) {
    const lines = text.trim().split('\n');
    if (lines.length === 0) return [];

    const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
    const data = [];

    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        if (values.length === headers.length) {
            const row = {};
            headers.forEach((header, index) => {
                const value = values[index].trim();
                row[header] = value === '' || value === 'null' ? null : value;
            });
            data.push(row);
        }
    }

    return data;
}

// Calculate comprehensive data statistics with quality metrics
function calculateStats(raw, cleaned) {
    const rawTotal = raw.length;
    const cleanedTotal = cleaned.length;

    // Count missing values and issues in raw data
    let rawMissing = 0;
    let rawNulls = 0;
    let totalFields = 0;
    let validFields = 0;

    raw.forEach(row => {
        let hasNull = false;
        Object.values(row).forEach(value => {
            totalFields++;
            if (value === null || value === '') {
                rawNulls++;
                if (!hasNull) {
                    rawMissing++;
                    hasNull = true;
                }
            } else {
                validFields++;
            }
        });
    });

    // Calculate quality metrics
    const quality = rawTotal > 0 ? ((cleanedTotal / rawTotal) * 100).toFixed(1) : 0;
    const completeness = totalFields > 0 ? ((validFields / totalFields) * 100).toFixed(1) : 0;
    const validity = rawTotal > 0 ? (((rawTotal - rawMissing) / rawTotal) * 100).toFixed(1) : 0;
    const consistency = rawTotal > 0 ? (((rawTotal - (rawTotal - cleanedTotal)) / rawTotal) * 100).toFixed(1) : 0;

    return {
        raw: {
            total: rawTotal,
            missing: rawMissing,
            nulls: rawNulls,
            completeness: parseFloat(completeness),
            validity: parseFloat(validity),
            consistency: parseFloat(consistency)
        },
        cleaned: {
            total: cleanedTotal,
            missing: 0,
            nulls: 0,
            completeness: 100,
            validity: 100,
            consistency: 100
        },
        quality: quality,
        removed: rawTotal - cleanedTotal
    };
}

// Generate analytics for cleaned data
function generateAnalytics(data) {
    if (data.length === 0) return {};

    const analytics = {};
    const keys = Object.keys(data[0]);

    keys.forEach(key => {
        const values = data.map(row => row[key]).filter(v => v !== null && v !== '');
        const uniqueValues = [...new Set(values)];

        analytics[key] = {
            uniqueCount: uniqueValues.length,
            totalCount: values.length,
            sampleValues: uniqueValues.slice(0, 5),
            nullCount: data.length - values.length
        };
    });

    return analytics;
}

// Update data quality indicators
function updateQualityIndicators(type, stats) {
    const data = stats[type];

    // Update completeness
    const completenessBar = document.getElementById(`${type}-completeness-bar`);
    const completenessValue = document.getElementById(`${type}-completeness`);
    if (completenessBar && completenessValue) {
        completenessBar.style.width = `${data.completeness}%`;
        completenessValue.textContent = `${data.completeness}%`;

        // Color coding based on quality
        if (data.completeness >= 95) {
            completenessBar.classList.add('success');
            completenessBar.classList.remove('warning', 'error');
        } else if (data.completeness >= 80) {
            completenessBar.classList.add('warning');
            completenessBar.classList.remove('success', 'error');
        } else {
            completenessBar.classList.add('error');
            completenessBar.classList.remove('success', 'warning');
        }
    }

    // Update validity
    const validityBar = document.getElementById(`${type}-validity-bar`);
    const validityValue = document.getElementById(`${type}-validity`);
    if (validityBar && validityValue) {
        validityBar.style.width = `${data.validity}%`;
        validityValue.textContent = `${data.validity}%`;

        if (data.validity >= 95) {
            validityBar.classList.add('success');
            validityBar.classList.remove('warning', 'error');
        } else if (data.validity >= 80) {
            validityBar.classList.add('warning');
            validityBar.classList.remove('success', 'error');
        } else {
            validityBar.classList.add('error');
            validityBar.classList.remove('success', 'warning');
        }
    }

    // Update consistency
    const consistencyBar = document.getElementById(`${type}-consistency-bar`);
    const consistencyValue = document.getElementById(`${type}-consistency`);
    if (consistencyBar && consistencyValue) {
        consistencyBar.style.width = `${data.consistency}%`;
        consistencyValue.textContent = `${data.consistency}%`;

        if (data.consistency >= 95) {
            consistencyBar.classList.add('success');
            consistencyBar.classList.remove('warning', 'error');
        } else if (data.consistency >= 80) {
            consistencyBar.classList.add('warning');
            consistencyBar.classList.remove('success', 'error');
        } else {
            consistencyBar.classList.add('error');
            consistencyBar.classList.remove('success', 'warning');
        }
    }
}

// Render analytics panel for cleaned data
function renderAnalytics(data) {
    const analyticsContainer = document.getElementById('cleaned-analytics');
    if (!analyticsContainer) return;

    const analytics = generateAnalytics(data);
    const analyticsHTML = Object.entries(analytics).map(([key, stats]) => `
        <div class="analytics-item">
            <div class="analytics-header">
                <i class="fas fa-database"></i>
                <strong>${key.charAt(0).toUpperCase() + key.slice(1)}</strong>
            </div>
            <div class="analytics-stats">
                <div class="stat-row">
                    <span>Unique Values:</span>
                    <span class="stat-value">${stats.uniqueCount.toLocaleString()}</span>
                </div>
                <div class="stat-row">
                    <span>Total Records:</span>
                    <span class="stat-value">${stats.totalCount.toLocaleString()}</span>
                </div>
                <div class="stat-row">
                    <span>Cardinality:</span>
                    <span class="stat-value">${((stats.uniqueCount / stats.totalCount) * 100).toFixed(1)}%</span>
                </div>
            </div>
        </div>
    `).join('');

    analyticsContainer.innerHTML = analyticsHTML;
}

// Load dataset
async function loadDataset(datasetName) {
    try {
        currentDataset = datasetName;
        const dataset = DATASETS[datasetName];

        // Show loading state
        showLoadingState();

        // Load raw data
        const rawResponse = await fetch(dataset.rawPath);
        const rawText = await rawResponse.text();
        rawData = parseCSV(rawText);

        // Load cleaned data
        const cleanedResponse = await fetch(dataset.cleanedPath);
        const cleanedText = await cleanedResponse.text();
        cleanedData = parseCSV(cleanedText);

        // Calculate statistics
        dataStats = calculateStats(rawData, cleanedData);

        // Reset pagination state
        paginationState.raw.filteredData = [...rawData];
        paginationState.raw.currentPage = 1;
        paginationState.cleaned.filteredData = [...cleanedData];
        paginationState.cleaned.currentPage = 1;

        // Update UI
        updateDatasetButtons();
        updateMetrics();
        updateQualityIndicators('raw', dataStats);
        updateQualityIndicators('cleaned', dataStats);
        renderAnalytics(cleanedData);
        updateColumnHeaders('raw', rawData[0]);
        updateColumnHeaders('cleaned', cleanedData[0]);
        renderTable('raw', 1);
        renderTable('cleaned', 1);

        hideLoadingState();

    } catch (error) {
        console.error('Error loading dataset:', error);
        showErrorState('Failed to load dataset. Please check if the CSV files exist.');
    }
}

// Show loading state
function showLoadingState() {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.innerHTML = `
        <div class="loading-spinner">
            <i class="fas fa-spinner fa-spin"></i>
            <p>Loading dataset...</p>
        </div>
    `;
    document.body.appendChild(overlay);
}

// Hide loading state
function hideLoadingState() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) overlay.remove();
}

// Show error state
function showErrorState(message) {
    hideLoadingState();
    alert(message);
}

// Update column headers dynamically
function updateColumnHeaders(type, sampleRow) {
    if (!sampleRow) return;

    const table = document.getElementById(`${type}-data-table`);
    const thead = table.querySelector('thead tr');
    thead.innerHTML = '';

    Object.keys(sampleRow).forEach(key => {
        const th = document.createElement('th');
        th.textContent = key.charAt(0).toUpperCase() + key.slice(1);
        thead.appendChild(th);
    });
}

// Data storage
// (Will be populated by loadDataset function)

// Pagination state
const paginationState = {
    raw: {
        currentPage: 1,
        itemsPerPage: 50,
        filteredData: [...rawData]
    },
    cleaned: {
        currentPage: 1,
        itemsPerPage: 50,
        filteredData: [...cleanedData]
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeDatasetSelector();
    initializeDataTables();
    initializeSearch();
    initializePagination();
    initializeComparison();

    // Load initial dataset
    loadDataset('field');
});

// Tab functionality
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');

            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// Initialize dataset selector
function initializeDatasetSelector() {
    const container = document.createElement('div');
    container.className = 'dataset-selector';
    container.innerHTML = `
        <div class="dataset-buttons">
            ${Object.keys(DATASETS).map(key => `
                <button class="dataset-btn" data-dataset="${key}">
                    <i class="fas ${DATASETS[key].icon}"></i>
                    <span>${DATASETS[key].name}</span>
                    <small>${DATASETS[key].description}</small>
                </button>
            `).join('')}
        </div>
    `;

    // Insert before raw data section
    const rawSection = document.getElementById('raw-data');
    rawSection.querySelector('.container').insertBefore(container, rawSection.querySelector('.section-header'));

    // Add event listeners
    container.querySelectorAll('.dataset-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            loadDataset(btn.dataset.dataset);
        });
    });
}

// Update dataset button states
function updateDatasetButtons() {
    const buttons = document.querySelectorAll('.dataset-btn');
    buttons.forEach(btn => {
        if (btn.dataset.dataset === currentDataset) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// Initialize comparison functionality
function initializeComparison() {
    // Add comparison toggle to both sections
    const rawSection = document.getElementById('raw-data');
    const cleanedSection = document.getElementById('cleaned-data');

    const comparisonToggle = `
        <button class="comparison-btn" id="toggle-comparison">
            <i class="fas fa-exchange-alt"></i> Compare Raw vs Cleaned
        </button>
    `;

    // Add to raw section controls
    const rawControls = rawSection.querySelector('.controls');
    if (rawControls) {
        rawControls.insertAdjacentHTML('beforeend', comparisonToggle);
    }

    // Add event listener
    setTimeout(() => {
        const btn = document.getElementById('toggle-comparison');
        if (btn) {
            btn.addEventListener('click', showComparison);
        }
    }, 100);
}

// Show comparison modal
function showComparison() {
    const modal = document.createElement('div');
    modal.className = 'comparison-modal';
    modal.id = 'comparison-modal';
    modal.innerHTML = `
        <div class="comparison-content">
            <div class="comparison-header">
                <h2><i class="fas fa-chart-bar"></i> Data Comparison: Raw vs Cleaned</h2>
                <button class="close-modal" onclick="closeComparison()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="comparison-body">
                <div class="comparison-stats">
                    <div class="comparison-card">
                        <h3>Raw Data</h3>
                        <div class="stat-group">
                            <div class="stat">
                                <span class="label">Total Records:</span>
                                <span class="value">${dataStats.raw.total.toLocaleString()}</span>
                            </div>
                            <div class="stat">
                                <span class="label">Records with Missing Values:</span>
                                <span class="value error">${dataStats.raw.missing.toLocaleString()}</span>
                            </div>
                            <div class="stat">
                                <span class="label">Total Null Fields:</span>
                                <span class="value error">${dataStats.raw.nulls.toLocaleString()}</span>
                            </div>
                        </div>
                    </div>
                    <div class="comparison-arrow">
                        <i class="fas fa-arrow-right"></i>
                        <div class="transform-label">Data Cleaning Pipeline</div>
                    </div>
                    <div class="comparison-card success">
                        <h3>Cleaned Data</h3>
                        <div class="stat-group">
                            <div class="stat">
                                <span class="label">Total Records:</span>
                                <span class="value">${dataStats.cleaned.total.toLocaleString()}</span>
                            </div>
                            <div class="stat">
                                <span class="label">Records with Missing Values:</span>
                                <span class="value success">0</span>
                            </div>
                            <div class="stat">
                                <span class="label">Total Null Fields:</span>
                                <span class="value success">0</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="comparison-summary">
                    <h3><i class="fas fa-info-circle"></i> Summary</h3>
                    <div class="summary-grid">
                        <div class="summary-item">
                            <i class="fas fa-trash-alt"></i>
                            <div>
                                <strong>${dataStats.removed.toLocaleString()}</strong>
                                <small>Records Removed</small>
                            </div>
                        </div>
                        <div class="summary-item">
                            <i class="fas fa-check-circle"></i>
                            <div>
                                <strong>${dataStats.quality}%</strong>
                                <small>Data Quality Score</small>
                            </div>
                        </div>
                        <div class="summary-item">
                            <i class="fas fa-database"></i>
                            <div>
                                <strong>${((dataStats.removed / dataStats.raw.total) * 100).toFixed(1)}%</strong>
                                <small>Removal Rate</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Close on outside click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeComparison();
        }
    });
}

// Close comparison modal
function closeComparison() {
    const modal = document.getElementById('comparison-modal');
    if (modal) modal.remove();
}

// Update metrics
function updateMetrics() {
    document.getElementById('total-records').textContent = dataStats.raw.total.toLocaleString();
    document.getElementById('cleaned-records').textContent = dataStats.cleaned.total.toLocaleString();
    document.getElementById('data-quality').textContent = dataStats.quality + '%';

    document.getElementById('raw-total').textContent = dataStats.raw.total.toLocaleString();
    document.getElementById('raw-missing').textContent = dataStats.raw.missing.toLocaleString();
    document.getElementById('raw-nulls').textContent = dataStats.raw.nulls.toLocaleString();
    document.getElementById('raw-issues').textContent = dataStats.removed.toLocaleString();

    document.getElementById('cleaned-total').textContent = dataStats.cleaned.total.toLocaleString();

    // Update cleaned data stats
    const cleanedMissingElem = document.getElementById('cleaned-missing');
    const cleanedNullsElem = document.getElementById('cleaned-nulls');
    const cleanedQualityElem = document.getElementById('cleaned-quality');

    if (cleanedMissingElem) cleanedMissingElem.textContent = '0';
    if (cleanedNullsElem) cleanedNullsElem.textContent = '0';
    if (cleanedQualityElem) cleanedQualityElem.textContent = '100%';

    // Calculate fields analyzed (number of columns)
    if (rawData.length > 0) {
        const fieldCount = Object.keys(rawData[0]).length;
        document.getElementById('fields-analyzed').textContent = fieldCount;
    }
}

// Initialize data tables
function initializeDataTables() {
    renderTable('raw', paginationState.raw.currentPage);
    renderTable('cleaned', paginationState.cleaned.currentPage);

    // Add limit change listeners
    document.getElementById('raw-limit').addEventListener('change', (e) => {
        paginationState.raw.itemsPerPage = parseInt(e.target.value);
        paginationState.raw.currentPage = 1;
        renderTable('raw', 1);
    });

    document.getElementById('cleaned-limit').addEventListener('change', (e) => {
        paginationState.cleaned.itemsPerPage = parseInt(e.target.value);
        paginationState.cleaned.currentPage = 1;
        renderTable('cleaned', 1);
    });
}

// Render table
function renderTable(type, page) {
    const state = paginationState[type];
    const data = state.filteredData;

    if (data.length === 0) {
        const tbody = document.getElementById(`${type}-data-body`);
        tbody.innerHTML = '<tr><td colspan="100" style="text-align: center; padding: 2rem;">No data available</td></tr>';
        return;
    }

    const startIndex = (page - 1) * state.itemsPerPage;
    const endIndex = startIndex + state.itemsPerPage;
    const pageData = data.slice(startIndex, endIndex);

    const tbody = document.getElementById(`${type}-data-body`);
    tbody.innerHTML = '';

    pageData.forEach(item => {
        const row = document.createElement('tr');
        const cells = Object.values(item).map(value => {
            if (value === null || value === '') {
                return '<span style="color: var(--error); font-weight: 600;">NULL</span>';
            }
            return value;
        }).join('</td><td>');
        row.innerHTML = `<td>${cells}</td>`;
        tbody.appendChild(row);
    });

    updatePaginationInfo(type);
}

// Initialize search functionality
function initializeSearch() {
    document.getElementById('raw-search').addEventListener('input', (e) => {
        filterData('raw', e.target.value.toLowerCase());
    });

    document.getElementById('cleaned-search').addEventListener('input', (e) => {
        filterData('cleaned', e.target.value.toLowerCase());
    });
}

// Filter data based on search term
function filterData(type, searchTerm) {
    const sourceData = type === 'raw' ? rawData : cleanedData;

    if (!searchTerm) {
        paginationState[type].filteredData = [...sourceData];
    } else {
        paginationState[type].filteredData = sourceData.filter(item => {
            return Object.values(item).some(value => {
                if (value === null) return false;
                return value.toString().toLowerCase().includes(searchTerm);
            });
        });
    }

    paginationState[type].currentPage = 1;
    renderTable(type, 1);
}

// Initialize pagination
function initializePagination() {
    // Raw data pagination
    document.getElementById('raw-prev').addEventListener('click', () => {
        if (paginationState.raw.currentPage > 1) {
            paginationState.raw.currentPage--;
            renderTable('raw', paginationState.raw.currentPage);
        }
    });

    document.getElementById('raw-next').addEventListener('click', () => {
        const maxPage = Math.ceil(paginationState.raw.filteredData.length / paginationState.raw.itemsPerPage);
        if (paginationState.raw.currentPage < maxPage) {
            paginationState.raw.currentPage++;
            renderTable('raw', paginationState.raw.currentPage);
        }
    });

    // Cleaned data pagination
    document.getElementById('cleaned-prev').addEventListener('click', () => {
        if (paginationState.cleaned.currentPage > 1) {
            paginationState.cleaned.currentPage--;
            renderTable('cleaned', paginationState.cleaned.currentPage);
        }
    });

    document.getElementById('cleaned-next').addEventListener('click', () => {
        const maxPage = Math.ceil(paginationState.cleaned.filteredData.length / paginationState.cleaned.itemsPerPage);
        if (paginationState.cleaned.currentPage < maxPage) {
            paginationState.cleaned.currentPage++;
            renderTable('cleaned', paginationState.cleaned.currentPage);
        }
    });
}

// Update pagination info
function updatePaginationInfo(type) {
    const state = paginationState[type];
    const maxPage = Math.ceil(state.filteredData.length / state.itemsPerPage);

    document.getElementById(`${type}-page-info`).textContent =
        `Page ${state.currentPage} of ${maxPage}`;

    // Update button states
    const prevBtn = document.getElementById(`${type}-prev`);
    const nextBtn = document.getElementById(`${type}-next`);

    prevBtn.disabled = state.currentPage === 1;
    nextBtn.disabled = state.currentPage === maxPage;
}

// Add smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ========================================
// ACADEMICS SECTION FUNCTIONALITY
// ========================================

// Initialize Academics Section
function initializeAcademics() {
    initializeSidebarNavigation();
    initializeFlowchartViewer();
    initializeCircuitViewer();
}

// Sidebar Navigation
function initializeSidebarNavigation() {
    const sidebarButtons = document.querySelectorAll('.sidebar-btn');
    const subjectContents = document.querySelectorAll('.subject-content');

    sidebarButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetSubject = button.getAttribute('data-subject');

            // Remove active class from all buttons and contents
            sidebarButtons.forEach(btn => btn.classList.remove('active'));
            subjectContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            document.getElementById(targetSubject).classList.add('active');
        });
    });
}

// Flowchart Viewer with Zoom and Pan
function initializeFlowchartViewer() {
    const flowchartButtons = document.querySelectorAll('.flowchart-btn');
    const flowchartImage = document.getElementById('flowchart-image');
    const flowchartWrapper = document.getElementById('flowchart-wrapper');
    const flowchartContainer = document.getElementById('flowchart-container');
    const flowchartTitle = document.getElementById('flowchart-title');
    const flowchartDescription = document.getElementById('flowchart-description');

    // Zoom controls
    const zoomInBtn = document.getElementById('zoom-in');
    const zoomOutBtn = document.getElementById('zoom-out');
    const zoomResetBtn = document.getElementById('zoom-reset');
    const zoomFullscreenBtn = document.getElementById('zoom-fullscreen');
    const zoomLevelDisplay = document.getElementById('zoom-level');

    // Zoom and pan state
    let scale = 1;
    let translateX = 0;
    let translateY = 0;
    let isDragging = false;
    let startX = 0;
    let startY = 0;
    let isFullscreen = false;

    const MIN_SCALE = 0.5;
    const MAX_SCALE = 5;
    const SCALE_STEP = 0.25;

    // Flowchart data
    const flowcharts = [
        {
            image: 'flowcharts/algorithm1.png',
            title: 'Sorting Algorithm Flowchart',
            description: 'Visualization of bubble sort algorithm with time complexity analysis'
        },
        // {
        //     image: 'flowcharts/algorithm2.png',
        //     title: 'Search Algorithm Flowchart',
        //     description: 'Binary search algorithm implementation and complexity breakdown'
        // },
        // {
        //     image: 'flowcharts/algorithm3.png',
        //     title: 'Graph Traversal Flowchart',
        //     description: 'Depth-first search (DFS) and breadth-first search (BFS) algorithms'
        // }
    ];

    // Load first flowchart by default
    if (flowcharts.length > 0 && flowchartTitle && flowchartDescription) {
        flowchartTitle.textContent = flowcharts[0].title;
        flowchartDescription.textContent = flowcharts[0].description;
    }

    // Update transform
    function updateTransform() {
        if (flowchartImage) {
            flowchartImage.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
            zoomLevelDisplay.textContent = `${Math.round(scale * 100)}%`;
        }
    }

    // Reset zoom and pan
    function resetZoom() {
        scale = 1;
        translateX = 0;
        translateY = 0;
        updateTransform();
    }

    // Zoom in
    function zoomIn() {
        if (scale < MAX_SCALE) {
            scale = Math.min(scale + SCALE_STEP, MAX_SCALE);
            updateTransform();
        }
    }

    // Zoom out
    function zoomOut() {
        if (scale > MIN_SCALE) {
            scale = Math.max(scale - SCALE_STEP, MIN_SCALE);
            updateTransform();
        }
    }

    // Toggle fullscreen
    function toggleFullscreen() {
        isFullscreen = !isFullscreen;

        if (isFullscreen) {
            flowchartWrapper.classList.add('fullscreen');
            zoomFullscreenBtn.innerHTML = '<i class="fas fa-compress"></i>';
            zoomFullscreenBtn.title = 'Exit Fullscreen';
        } else {
            flowchartWrapper.classList.remove('fullscreen');
            zoomFullscreenBtn.innerHTML = '<i class="fas fa-expand"></i>';
            zoomFullscreenBtn.title = 'Fullscreen';
        }
    }

    // Button event listeners
    if (zoomInBtn) zoomInBtn.addEventListener('click', zoomIn);
    if (zoomOutBtn) zoomOutBtn.addEventListener('click', zoomOut);
    if (zoomResetBtn) zoomResetBtn.addEventListener('click', resetZoom);
    if (zoomFullscreenBtn) zoomFullscreenBtn.addEventListener('click', toggleFullscreen);

    // Mouse wheel zoom
    if (flowchartWrapper) {
        flowchartWrapper.addEventListener('wheel', (e) => {
            if (flowchartImage.classList.contains('loaded')) {
                e.preventDefault();

                const delta = e.deltaY > 0 ? -SCALE_STEP : SCALE_STEP;
                const newScale = Math.max(MIN_SCALE, Math.min(MAX_SCALE, scale + delta));

                if (newScale !== scale) {
                    scale = newScale;
                    updateTransform();
                }
            }
        }, { passive: false });

        // Pan functionality - Mouse events
        flowchartWrapper.addEventListener('mousedown', (e) => {
            if (flowchartImage.classList.contains('loaded') && scale > 1) {
                isDragging = true;
                startX = e.clientX - translateX;
                startY = e.clientY - translateY;
                flowchartWrapper.classList.add('grabbing');
                e.preventDefault();
            }
        });

        document.addEventListener('mousemove', (e) => {
            if (isDragging) {
                translateX = e.clientX - startX;
                translateY = e.clientY - startY;
                updateTransform();
            }
        });

        document.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                flowchartWrapper.classList.remove('grabbing');
            }
        });

        // Pan functionality - Touch events for mobile
        let touchStartX = 0;
        let touchStartY = 0;

        flowchartWrapper.addEventListener('touchstart', (e) => {
            if (flowchartImage.classList.contains('loaded') && scale > 1) {
                isDragging = true;
                touchStartX = e.touches[0].clientX - translateX;
                touchStartY = e.touches[0].clientY - translateY;
            }
        });

        flowchartWrapper.addEventListener('touchmove', (e) => {
            if (isDragging) {
                e.preventDefault();
                translateX = e.touches[0].clientX - touchStartX;
                translateY = e.touches[0].clientY - touchStartY;
                updateTransform();
            }
        }, { passive: false });

        flowchartWrapper.addEventListener('touchend', () => {
            isDragging = false;
        });
    }

    // Flowchart switching
    flowchartButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            flowchartButtons.forEach(btn => btn.classList.remove('active'));

            // Add active class to clicked button
            button.classList.add('active');

            // Update flowchart display
            const flowchart = flowcharts[index];
            flowchartImage.src = flowchart.image;
            flowchartTitle.textContent = flowchart.title;
            flowchartDescription.textContent = flowchart.description;

            // Reset zoom when switching flowcharts
            resetZoom();

            // Handle image loading
            flowchartImage.onload = function() {
                flowchartImage.classList.add('loaded');
                document.querySelector('.flowchart-placeholder').style.display = 'none';
            };

            flowchartImage.onerror = function() {
                flowchartImage.classList.remove('loaded');
                document.querySelector('.flowchart-placeholder').style.display = 'block';
            };
        });
    });

    // Try to load first flowchart
    flowchartImage.onload = function() {
        flowchartImage.classList.add('loaded');
        document.querySelector('.flowchart-placeholder').style.display = 'none';
    };

    flowchartImage.onerror = function() {
        flowchartImage.classList.remove('loaded');
        document.querySelector('.flowchart-placeholder').style.display = 'block';
    };

    // ESC key to exit fullscreen
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isFullscreen) {
            toggleFullscreen();
        }
    });
}

// Circuit Viewer
function initializeCircuitViewer() {
    const reloadButton = document.getElementById('reload-circuit');
    const circuitFrame = document.getElementById('logisim-frame');

    // Reload circuit button
    if (reloadButton) {
        reloadButton.addEventListener('click', () => {
            circuitFrame.src = circuitFrame.src;
        });
    }

    // Check if circuit iframe loads successfully
    circuitFrame.onload = function() {
        // Only hide placeholder if the URL is not the placeholder URL
        if (!circuitFrame.src.includes('placeholder')) {
            circuitFrame.classList.add('loaded');
            const placeholder = document.querySelector('.circuit-placeholder');
            if (placeholder) {
                placeholder.style.display = 'none';
            }
        }
    };
}

// Initialize academics when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeAcademics);
} else {
    initializeAcademics();
}

// ========================================
// ANALYTICS DASHBOARD NAVIGATION
// ========================================

function initializeAnalyticsNavigation() {
    // Get all analytics navigation buttons
    const analyticsNavButtons = document.querySelectorAll('.analytics-nav .sidebar-btn');
    const analyticsSections = document.querySelectorAll('.analytics-section');

    // Handle analytics sub-navigation
    analyticsNavButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetSection = button.getAttribute('data-analytics');

            // Update active button
            analyticsNavButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Show target analytics section
            analyticsSections.forEach(section => {
                section.classList.remove('active');
                if (section.id === targetSection) {
                    section.classList.add('active');
                }
            });

            // Smooth scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });
}

// Initialize analytics navigation when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeAnalyticsNavigation);
} else {
    initializeAnalyticsNavigation();
}
