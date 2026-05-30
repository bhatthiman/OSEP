const API = "http://127.0.0.1:8000"

export async function loadProject() {

  await fetch(`${API}/projects/load`, {
    method: "POST"
  })

  const response = await fetch(
    `${API}/projects/active`
  )

  return await response.json()
}

export async function getComponentSchema(type) {

  const response = await fetch(
    `${API}/components/${type}/schema`
  )

  return await response.json()
}

export async function updateComponent(
  componentId,
  payload
) {

  const response = await fetch(
    `${API}/projects/components/${componentId}`,
    {
      method: "PATCH",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify(payload)
    }
  )

  return await response.json()
}

export function buildPreviewUrl(path) {

  return `${API}${path}`
}
export async function addComponent(
  component
) {

  const response = await fetch(
    "http://127.0.0.1:8000/projects/components",
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify(
        component
      )
    }
  )

  return await response.json()
}
export async function newProject() {

  const response = await fetch(
    "http://127.0.0.1:8000/projects/new",
    {
      method: "POST"
    }
  )

  return await response.json()
}
export async function getProjectPreview() {

  const response = await fetch(
    "http://127.0.0.1:8000/projects/preview"
  )

  return await response.json()
}
export async function saveProject(
  project
) {

  const response = await fetch(
    "http://127.0.0.1:8000/projects/save",
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json"
      },

      body: JSON.stringify(
        project
      )
    }
  )

  return await response.json()
}


