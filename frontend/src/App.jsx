import {
  useEffect,
  useState
} from "react"

import Viewer from "./viewer/Viewer"

import ComponentLibrary
from "./components/ComponentLibrary"

import ProjectStructure
from "./components/ProjectStructure"

import PropertyEditor
from "./components/PropertyEditor"

import {

  loadProject,

  newProject,

  saveProject,

  updateComponent,

  buildPreviewUrl,

  addComponent,

  getComponentSchema,

  getProjectPreview

} from "./services/api"


function App() {

  // ----------------------------------
  // Project State
  // ----------------------------------

  const [project, setProject] =
    useState({
      project: {
        name: "Untitled"
      },

      components: []
    })

  const [selected, setSelected] =
    useState(null)

  const [schema, setSchema] =
    useState(null)

  const [previewUrl, setPreviewUrl] =
    useState(null)

  // ----------------------------------
  // Load Schema
  // ----------------------------------

  useEffect(() => {

    if (!selected) {

      setSchema(null)

      return
    }

    async function loadSchema() {

      const schemaData =
        await getComponentSchema(
          selected.type
        )

      setSchema(schemaData)
    }

    loadSchema()

  }, [selected])

  // ----------------------------------
  // New Project
  // ----------------------------------

  async function handleNewProject() {

    const projectData =
      await newProject()

    setProject(projectData)

    setSelected(null)

    setSchema(null)

    setPreviewUrl(null)
  }

  // ----------------------------------
  // Load Example Project
  // ----------------------------------

  async function handleLoadProject() {

    const projectData =
      await loadProject()

    setProject(projectData)

    setSelected(null)

    setSchema(null)

    try {

      const preview =
        await getProjectPreview()

      setPreviewUrl(
        buildPreviewUrl(
          preview.preview_file
        )
      )
      console.log(
        buildPreviewUrl(
          preview.preview_file
        )
      )

    } catch (err) {

      console.log(
        "Preview unavailable"
      )
    }
  }

  // ----------------------------------
  // Save Project
  // ----------------------------------

  async function handleSaveProject() {

    try {

      await saveProject(project)

      alert(
        "Project saved"
      )

    } catch (err) {

      console.log(err)

      alert(
        "Save failed"
      )
    }
  }

  // ----------------------------------
  // Generate Preview
  // ----------------------------------

  async function handleGeneratePreview() {

    if (!selected) {

      alert(
        "Select component first"
      )

      return
    }

    try {

      // --------------------------
      // Push selected component
      // --------------------------

      await updateComponent(
        selected.id,
        selected.data
      )

      // --------------------------
      // Generate full assembly
      // --------------------------

      const preview =
        await getProjectPreview()

      setPreviewUrl(
        buildPreviewUrl(
          preview.preview_file
        )
      )

    } catch (err) {

      console.log(err)

      alert(
        "Component data incomplete or invalid"
      )
    }
  }

  // ----------------------------------
  // Update Nested Property
  // ----------------------------------

  function setByPath(
    obj,
    path,
    value
  ) {

    const keys = path

    let current = obj

    for (
      let i = 0;
      i < keys.length - 1;
      i++
    ) {

      const key = keys[i]

      // ------------------------
      // Create Array Index
      // ------------------------

      if (
        typeof keys[i + 1]
          === "number"
      ) {

        if (
          current[key]
            === undefined
        ) {

          current[key] = []
        }

      } else {

        if (
          current[key]
            === undefined
        ) {

          current[key] = {}
        }
      }

      current = current[key]
    }

    current[
      keys[keys.length - 1]
    ] = value
  }

  // ----------------------------------
  // Handle Property Change
  // ----------------------------------

  function handleChange(
    path,
    value
  ) {

    const updated =
      structuredClone(selected)

    if (!updated.data) {

      updated.data = {}
    }

    setByPath(
      updated.data,
      path,
      value
    )

    setSelected(updated)

    // --------------------------------
    // Update Project State
    // --------------------------------

    const updatedComponents =
      project.components.map(c => {

        if (
          c.id === updated.id
        ) {

          return updated
        }

        return c
      })

    const updatedProject = {

      ...project,

      components:
        updatedComponents
    }

    setProject(updatedProject)
  }

  // ----------------------------------
  // Select Component
  // ----------------------------------

  function handleSelect(
    component
  ) {

    setSelected(component)
  }

  // ----------------------------------
  // Generate Component ID
  // ----------------------------------

  function generateComponentId(
    type
  ) {

    const sameType =
      project.components.filter(
        c => c.type === type
      )

    return `${type}_${sameType.length + 1}`
  }

  // ----------------------------------
  // Add Empty Component
  // ----------------------------------

  async function handleAddComponent(
    type
  ) {

    const component = {

      id:
        generateComponentId(
          type
        ),

      type,

      data: {}
    }

    const created =
      await addComponent(
        component
      )

    const updatedProject = {

      ...project,

      components: [
        ...project.components,
        created
      ]
    }

    setProject(updatedProject)

    setSelected(created)
  }

  // ----------------------------------
  // UI
  // ----------------------------------

  return (

    <div
      style={{
        display: "grid",

        gridTemplateColumns:
          "220px 220px 1fr",

        gridTemplateRows:
          "60px 1fr 320px",

        height: "100vh"
      }}
    >

      {/* -------------------------------- */}
      {/* Toolbar */}
      {/* -------------------------------- */}

      <div
        style={{
          gridColumn:
            "1 / span 3",

          borderBottom:
            "1px solid #ccc",

          display: "flex",

          alignItems: "center",

          padding: "0 10px",

          gap: "10px"
        }}
      >

        <button
          onClick={
            handleNewProject
          }
        >

          New Project

        </button>

        <button
          onClick={
            handleLoadProject
          }
        >

          Load Project

        </button>

        <button
          onClick={
            handleSaveProject
          }
        >

          Save Project

        </button>

        <button
          onClick={
            handleGeneratePreview
          }
        >

          Update View

        </button>

        <div>

          Project:
          {" "}
          {
            project.project.name
          }

        </div>

      </div>

      {/* -------------------------------- */}
      {/* Component Library */}
      {/* -------------------------------- */}

      <div
        style={{
          borderRight:
            "1px solid #ccc",

          padding: "10px",

          overflow: "auto"
        }}
      >

        <ComponentLibrary
          componentTypes={[
            "cylinder",
            "head"
          ]}

          onAdd={
            handleAddComponent
          }
        />

      </div>

      {/* -------------------------------- */}
      {/* Project Structure */}
      {/* -------------------------------- */}

      <div
        style={{
          borderRight:
            "1px solid #ccc",

          padding: "10px",

          overflow: "auto"
        }}
      >

        <ProjectStructure
          components={
            project.components
          }

          selectedId={
            selected?.id
          }

          onSelect={
            handleSelect
          }
        />

      </div>

      {/* -------------------------------- */}
      {/* Viewer */}
      {/* -------------------------------- */}

      <div
        style={{
          overflow: "hidden"
        }}
      >

        {
          previewUrl ? (

            <Viewer
              stlUrl={previewUrl}
            />

          ) : (

            <div
              style={{
                display: "flex",

                alignItems:
                  "center",

                justifyContent:
                  "center",

                height: "100%"
              }}
            >

              No Preview

            </div>
          )
        }

      </div>

      {/* -------------------------------- */}
      {/* Property Editor */}
      {/* -------------------------------- */}

      <div
        style={{
          gridColumn:
            "1 / span 3",

          borderTop:
            "1px solid #ccc",

          overflow: "auto",

          padding: "20px"
        }}
      >

        <PropertyEditor
          schema={schema}

          component={selected}

          onChange={
            handleChange
          }
        />

      </div>

    </div>
  )
}

export default App
