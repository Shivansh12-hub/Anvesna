// 📌 Risk Assessment Form Handling
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("assessmentForm");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const inputs = form.querySelectorAll("input");
      let age = parseInt(inputs[0].value);
      let systolic = parseInt(inputs[1].value);
      let diastolic = parseInt(inputs[2].value);
      let sugar = parseInt(inputs[3].value);
      let temp = parseFloat(inputs[4].value);

      let riskScore = 0;

      if (age > 35) riskScore += 2;
      if (systolic > 140 || diastolic > 90) riskScore += 3;
      if (sugar > 140) riskScore += 2;
      if (temp > 100.4) riskScore += 1;

      let category = "Low Risk";
      let cssClass = "risk-low";

      if (riskScore >= 3 && riskScore <= 5) {
        category = "Medium Risk";
        cssClass = "risk-medium";
      }
      if (riskScore > 5) {
        category = "High Risk";
        cssClass = "risk-high";
      }

      const resultBox = document.getElementById("resultBox");
      resultBox.style.display = "block";
      resultBox.className = `risk-result ${cssClass}`;
      resultBox.innerHTML = `
        Risk Score: ${riskScore}<br>
        Status: ${category}<br>
        ${category === "Low Risk" ? "✅ Continue regular checkups." : ""}
        ${category === "Medium Risk" ? "⚠ Please consult your doctor soon." : ""}
        ${category === "High Risk" ? "🚨 Immediate medical attention required!" : ""}
      `;

      // Update localStorage for Home stats
      let total = parseInt(localStorage.getItem("totalAssessments") || 0) + 1;
      localStorage.setItem("totalAssessments", total);
      localStorage.setItem("lastRiskScore", riskScore);
    });
  }

  // 📌 Reports Handling
  const reportTitle = document.getElementById("reportTitle");
  const reportDetails = document.getElementById("reportDetails");
  const reportsList = document.getElementById("reportsList");

  if (reportTitle && reportDetails && reportsList) {
    window.addReport = function () {
      if (reportTitle.value.trim() === "" || reportDetails.value.trim() === "") {
        alert("Please fill both fields!");
        return;
      }

      const reportCard = document.createElement("div");
      reportCard.className = "report-card";
      reportCard.innerHTML = `
        <div class="report-header">
          <span>${reportTitle.value}</span>
          <span>${new Date().toLocaleDateString()}</span>
        </div>
        <p>${reportDetails.value}</p>
      `;

      reportsList.prepend(reportCard);

      // Clear inputs
      reportTitle.value = "";
      reportDetails.value = "";
    };
  }

  // 📌 Update Home Page Stats
  if (document.getElementById("totalAssessments")) {
    document.getElementById("totalAssessments").innerText =
      localStorage.getItem("totalAssessments") || 0;
  }
  if (document.getElementById("lastRiskScore")) {
    document.getElementById("lastRiskScore").innerText =
      localStorage.getItem("lastRiskScore") || "--";
  }
});
