// Configuration - Update this URL to match your Flask API
const API_BASE_URL = "http://127.0.0.1:5000" // Change this to your Flask server URL

// Utility Functions
function scrollToSection(sectionId) {
  document.getElementById(sectionId).scrollIntoView({
    behavior: "smooth",
  })
}

function toggleSection(sectionId) {
  // Hide services section
  document.getElementById("services").style.display = "none"

  // Hide all prediction sections
  const sections = ["education", "finance", "entertainment"]
  sections.forEach((id) => {
    document.getElementById(id).classList.add("hidden")
  })

  // Show the selected section
  document.getElementById(sectionId).classList.remove("hidden")

  // Scroll to the section
  document.getElementById(sectionId).scrollIntoView({
    behavior: "smooth",
  })
}

function closeSection() {
  // Hide all prediction sections
  const sections = ["education", "finance", "entertainment"]
  sections.forEach((id) => {
    document.getElementById(id).classList.add("hidden")
  })

  // Show services section
  document.getElementById("services").style.display = "block"

  // Scroll to services
  scrollToSection("services")
}

function toggleForm(formId) {
  const form = document.getElementById(formId)
  form.classList.toggle("hidden")
}

function showLoading() {
  document.getElementById("loadingModal").classList.remove("hidden")
}

function hideLoading() {
  document.getElementById("loadingModal").classList.add("hidden")
}

function redirectToResults(result, inputData, type) {
  localStorage.setItem(
    "predictionResult",
    JSON.stringify({
      type: type,
      data: inputData,
      result: result,
      timestamp: new Date().toISOString(),
    }),
  )

  // Redirect to results page
  window.location.href = "results.html"
}

// Form Submission Functions
async function submitStudentForm(event) {
  event.preventDefault()
  showLoading()

  const formData = new FormData(event.target)

  // Student Performance model expects: ['Hours Studied', 'Previous Scores', 'Extracurricular Activities', 'Sleep Hours', 'Sample Question Papers Practiced']
  const requiredFields = [
    "Hours Studied",
    "Previous Scores",
    "Extracurricular Activities",
    "Sleep Hours",
    "Sample Question Papers Practiced",
  ]

  const dataObject = {}

  console.log("[v0] Student form validation starting...")

  for (const field of requiredFields) {
    const value = formData.get(field)
    console.log(`[v0] Student field: ${field} = "${value}" (type: ${typeof value})`)

    // Check for empty, null, undefined, or whitespace-only values
    if (value === "" || value === null || value === undefined || (typeof value === "string" && value.trim() === "")) {
      hideLoading()
      alert(`Please fill in all fields. Missing: ${field}`)
      return
    }

    if (field === "Extracurricular Activities") {
      dataObject[field] = value // Keep as string ("Yes" or "No")
    } else {
      // Convert to number and validate it's a valid number
      const numValue = Number.parseFloat(value)
      if (isNaN(numValue)) {
        hideLoading()
        alert(`Please enter a valid number for: ${field}`)
        return
      }
      dataObject[field] = numValue
    }
  }

  console.log("[v0] Student data object being sent:", dataObject)

  try {
    const response = await fetch(`${API_BASE_URL}/Studentperformance`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dataObject),
    })

    const result = await response.json()
    hideLoading()

    if (response.ok) {
      redirectToResults(result, { fields: requiredFields, values: Object.values(dataObject) }, "student")
    } else {
      console.log("[v0] Student API error:", result)
      alert(`Error: ${result.error}`)
    }
  } catch (error) {
    console.log("[v0] Student network error:", error)
    hideLoading()
    redirectToResults(
      { error: error.message },
      { fields: requiredFields, values: Object.values(dataObject) },
      "student",
    )
  }
}

async function submitPlacementForm(event) {
  event.preventDefault()
  showLoading()

  const formData = new FormData(event.target)

  // Placement model expects: ['CGPA', 'Internships', 'Projects', 'Workshops/Certifications', 'AptitudeTestScore', 'SoftSkillsRating', 'ExtracurricularActivities', 'PlacementTraining', 'SSC_Marks', 'HSC_Marks']
  const requiredFields = [
    "CGPA",
    "Internships",
    "Projects",
    "Workshops/Certifications",
    "AptitudeTestScore",
    "SoftSkillsRating",
    "ExtracurricularActivities",
    "PlacementTraining",
    "SSC_Marks",
    "HSC_Marks",
  ]

  const dataObject = {}

  for (const field of requiredFields) {
    const value = formData.get(field)
    console.log(`[v0] Placement field: ${field} = "${value}"`)

    if (value === "" || value === null || value === undefined) {
      hideLoading()
      alert(`Please fill in all fields. Missing: ${field}`)
      return
    }

    // Keep categorical fields as strings, convert numeric fields to numbers
    if (field === "ExtracurricularActivities" || field === "PlacementTraining") {
      dataObject[field] = value // Keep as string ("Yes" or "No")
    } else {
      dataObject[field] = Number.parseFloat(value)
    }
  }

  console.log("[v0] Placement data object being sent:", dataObject)

  try {
    const response = await fetch(`${API_BASE_URL}/placementPrediction`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dataObject),
    })

    const result = await response.json()
    hideLoading()

    if (response.ok) {
      redirectToResults(result, { fields: requiredFields, values: Object.values(dataObject) }, "placement")
    } else {
      console.log("[v0] Placement API error:", result)
      alert(`Error: ${result.error}`)
    }
  } catch (error) {
    console.log("[v0] Placement network error:", error)
    hideLoading()
    redirectToResults(
      { error: error.message },
      { fields: requiredFields, values: Object.values(dataObject) },
      "placement",
    )
  }
}

async function submitBudgetForm(event) {
  event.preventDefault()
  showLoading()

  const formData = new FormData(event.target)

  // Budget model expects: ['Eating_Out', 'Entertainment', 'Miscellaneous', 'Groceries', 'Transport', 'Desired_Savings', 'Disposable_Income']
  const requiredFields = [
    "Eating_Out",
    "Entertainment",
    "Miscellaneous",
    "Groceries",
    "Transport",
    "Desired_Savings",
    "Disposable_Income",
  ]

  const dataObject = {}

  for (const field of requiredFields) {
    const value = formData.get(field)
    console.log(`[v0] Budget field: ${field} = "${value}"`)

    if (value === "" || value === null || value === undefined) {
      hideLoading()
      alert(`Please fill in all fields. Missing: ${field}`)
      return
    }
    dataObject[field] = Number.parseFloat(value)
  }

  console.log("[v0] Budget data object being sent:", dataObject)

  try {
    const response = await fetch(`${API_BASE_URL}/BudgetAnalysis`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dataObject),
    })

    console.log("[v0] Budget API response status:", response.status)
    console.log("[v0] Budget API response headers:", response.headers)

    const responseText = await response.text()
    console.log("[v0] Budget API raw response:", responseText)

    let result
    try {
      result = JSON.parse(responseText)
      console.log("[v0] Budget API parsed result:", result)
    } catch (parseError) {
      console.log("[v0] Budget API JSON parse error:", parseError)
      hideLoading()
      alert(`Server returned invalid JSON. Raw response: ${responseText}`)
      return
    }

    hideLoading()

    if (response.ok) {
      redirectToResults(result, { fields: requiredFields, values: Object.values(dataObject) }, "budget")
    } else {
      console.log("[v0] Budget API error:", result)
      alert(`Error: ${result.error || "Unknown error"}`)
    }
  } catch (error) {
    console.log("[v0] Budget network error:", error)
    hideLoading()
    redirectToResults({ error: error.message }, { fields: requiredFields, values: Object.values(dataObject) }, "budget")
  }
}

async function submitMovieForm(event) {
  event.preventDefault()
  showLoading()

  const formData = new FormData(event.target)
  const title = formData.get("title")

  console.log(`[v0] Movie form title: "${title}" (type: ${typeof title})`)

  if (!title || title.trim() === "") {
    hideLoading()
    alert("Please enter a movie title")
    return
  }

  const movieData = { title: title.trim() }
  console.log("[v0] Movie form data being sent:", JSON.stringify(movieData, null, 2))

  try {
    const titleEncoded = encodeURIComponent(title.trim())
    const url = `${API_BASE_URL}/moveRecommendation?title=${titleEncoded}`

    const response = await fetch(url, {
      method: "GET",
      headers: {
       "Content-Type": "application/json",
        },
})


    const result = await response.json()
    hideLoading()

    if (response.ok) {
      redirectToResults(result, { title: title }, "movie")
    } else {
      console.log("[v0] Movie API error:", result)
      alert(`Error: ${result.error}`)
    }
  } catch (error) {
    console.log("[v0] Movie network error:", error)
    hideLoading()
    redirectToResults({ error: error.message }, { title: title }, "movie")
  }
}

// Smooth scrolling for navigation links
document.addEventListener("DOMContentLoaded", () => {
  // Add smooth scrolling to all navigation links
  const navLinks = document.querySelectorAll(".nav-menu a")
  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault()
      const targetId = this.getAttribute("href").substring(1)

      if (targetId === "services") {
        // Show services section and hide prediction sections
        document.getElementById("services").style.display = "block"
        const sections = ["education", "finance", "entertainment"]
        sections.forEach((id) => {
          document.getElementById(id).classList.add("hidden")
        })
      }

      scrollToSection(targetId)
    })
  })

  // Add form submission event listeners
  const forms = document.querySelectorAll("form")
  forms.forEach((form) => {
    const formContainer = form.closest(".form-container")
    if (formContainer) {
      const formId = formContainer.id
      if (formId === "student-form") {
        form.addEventListener("submit", submitStudentForm)
      } else if (formId === "placement-form") {
        form.addEventListener("submit", submitPlacementForm)
      } else if (formId === "budget-form") {
        form.addEventListener("submit", submitBudgetForm)
      } else if (formId === "movie-form") {
        form.addEventListener("submit", submitMovieForm)
      }
    }
  })
})
