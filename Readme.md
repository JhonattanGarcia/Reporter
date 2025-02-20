# **Automated Report Generator** 📊  
(Last update 17-feb-2025)

## **Overview**  
This Python-based **Automated Report Generator** processes structured data from a CSV file, extracts key insights, and generates a **comprehensive PDF report** with **graphs, tables, and statistical analysis**. It allows users to **cross-analyze two data fields** while applying optional **filters** to refine the results.  

---

## **Features**  
- ✅ **CSV Data Processing** – Reads structured data and analyzes relationships between fields.  
- ✅ **Dynamic Cross-Analysis** – Compares two fields and applies optional filters.  
- ✅ **Customizable Visualizations** – Generates **bar charts** and **pie charts**.  
- ✅ **Automated Table Generation** – Displays the exact values used for each graph.  
- ✅ **Proactivity Analysis** – Calculates key statistics based on predefined conditions.  
- ✅ **Date Range Identification** – Automatically detects the **earliest and latest** date in the dataset.  
- ✅ **Configurable Parameters** – Adjust titles, filters, data ranking, and verbosity mode via `config.json`.  
- ✅ **PDF Export** – Generates a **professional, structured report** with graphs and insights.  

---

## **How It Works**  
1. **Configuration:** Modify `config.json` to define the dataset, fields to analyze, and filter options.  
2. **Execution:** Run the script with:  
   ```sh
   python runme.py
3. **Open the file:** The file will be in the destination folder assigned in config.json

# **Settings** 
Modify config.json to customize report behavior
```json
{
  "input_csv": "data/dataset.csv",
  "output_folder": "output",
  "output_tittle": "Analysis",
  "campo_fechas": "Date",
  "test_mode": 1,
  "top": 5,
  "author": "Your Name"
}
```
|Parameter	|Description|
|------|-----|
|input_csv	|Path to the CSV dataset.|
|output_folder	|Directory for storing the generated report.|
|output_tittle	|Base name for the output PDF.|
|campo_fechas	|Date field used for time-based analysis.|
|test_mode	|1 enables console logs, 0 runs silently.|
|top	|Number of results to display in ranking.|
|author|	Name of the report creator.|

📌 Data Analysis Report – Evaluated from 2025-02-08 to 2025-02-18

📊 Cross-Analysis: Field A vs. Field B
[Graph - Bar Chart]

📋 Data Table:
| Category  | Count |
|-----------|-------|
| Value 1   | 35    |
| Value 2   | 27    |
| Value 3   | 19    |

📊 Additional Insights
[Graph - Pie Chart]

📋 Data Table:
| Category  | Count |
|-----------|-------|
| Value X   | 55    |
| Value Y   | 42    |
| Value Z   | 33    |

