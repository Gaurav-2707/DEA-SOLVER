# 📈 Data Envelopment Analysis (DEA) Dashboard

This is a simple and interactive **Streamlit** app to perform **Data Envelopment Analysis (DEA)** on Decision-Making Units (DMUs). The app supports:
- Excel file upload
- Selection of input and output columns
- Efficiency calculation using linear programming via **CVXPY**
- Benchmark DMUs and input slack suggestions for inefficient units

---

## 🧰 Features

✅ Upload `.xlsx` file with DMU data  
✅ Select multiple input and output variables  
✅ Solve input-oriented DEA using CVXPY  
✅ Identify efficient and inefficient DMUs  
✅ Show benchmarks and λ-weights  
✅ Display input slack recommendations  

---

## 📁 File Format

The Excel file must follow this format:

| DMU Name | Input 1 | Input 2 | ... | Output 1 | Output 2 | ... |
|----------|---------|---------|-----|----------|----------|-----|
| DMU A    | 30      | 10      | ... | 50       | 20       | ... |
| DMU B    | 20      | 12      | ... | 60       | 22       | ... |
| ...      | ...     | ...     | ... | ...      | ...      | ... |

- **First column**: DMU names  
- **Next columns**: Inputs  
- **Remaining columns**: Outputs
