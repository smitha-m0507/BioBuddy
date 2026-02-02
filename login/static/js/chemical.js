document.addEventListener("DOMContentLoaded", function () {
  let lastClickedCard = null;
  let safetyAlert = document.getElementById("safetyAlert");
  let alertMessageSpan = document.getElementById("alertMessage");

  if (!safetyAlert || !alertMessageSpan) {
      console.error("Safety alert elements not found!");
      return;
  }

  const safetyMessages = {
      "Sodium Chloride": "Sodium Chloride is safe under normal conditions, but avoid ingesting large quantities. <br> Safety Measures: Keep away from eyes and wash hands after handling.",
      "Sulfuric Acid": "Sulfuric Acid is highly corrosive. Always wear gloves and goggles. <br> Safety Measures: In case of contact, rinse with water immediately. Use in well-ventilated areas.",
      "Ethanol": "Ethanol is highly flammable. Avoid open flames. <br> Safety Measures: Keep in a cool, dry place and store away from heat sources.",
      "Hydrochloric Acid": "Highly corrosive acid used in chemical reactions. <br> Safety Measures: Wear gloves, avoid inhaling fumes.",
      "Acetone": "A solvent used in cleaning. <br> Safety Measures: Highly flammable, keep away from heat and flames.",
      "Ammonia": "Common cleaner, but produces strong fumes. <br> Safety Measures: Avoid inhalation, do not mix with bleach.",
      "Sodium Hydroxide": "Strong base used in soap making. <br> Safety Measures: Highly caustic, wear protective gloves and goggles.",
      "Benzene": "Used in industrial processes. <br> Safety Measures: Carcinogenic, avoid prolonged exposure.",
      "Chloroform": "Lab solvent with anesthetic properties. <br> Safety Measures: Avoid inhalation, can cause unconsciousness.",
      "Formaldehyde": "Preservative for biological specimens. <br> Safety Measures: Irritant and potential carcinogen, use in ventilated areas."
  };

  function toggleSafetyAlert(chemicalName) {
      console.log("toggleSafetyAlert() called for:", chemicalName);
      
      // If the same card is clicked again, hide the alert
      if (lastClickedCard === chemicalName) {
          safetyAlert.style.display = "none";
          lastClickedCard = null;
          return;
      }

      // Show the new alert message
      alertMessageSpan.innerHTML = safetyMessages[chemicalName] || "Safety measures not available.";
      safetyAlert.style.display = "block";

      lastClickedCard = chemicalName;
  }

  window.searchChemicals = function () {
      let input = document.getElementById("searchBar").value.toLowerCase();
      let cards = document.getElementsByClassName("chemical-card");
      for (let i = 0; i < cards.length; i++) {
          let title = cards[i].getElementsByClassName("card-title")[0].innerText.toLowerCase();
          cards[i].style.display = title.includes(input) ? "block" : "none";
      }
  };

  const chemicalCards = document.querySelectorAll('.chemical-card');
  chemicalCards.forEach(card => {
      card.addEventListener('click', function () {
          const chemicalName = this.querySelector('.card-title').innerText;
          toggleSafetyAlert(chemicalName);
      });
  });
});
