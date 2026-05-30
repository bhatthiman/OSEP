import {
  useEffect,
  useState
} from "react"

function FieldInput({
  type,
  value,
  onCommit
}) {

  const [localValue, setLocalValue] =
    useState(value ?? "")

  useEffect(() => {

    setLocalValue(value ?? "")

  }, [value])

  return (

    <input
      type={type}

      value={localValue}

      onChange={(e) =>
        setLocalValue(
          e.target.value
        )
      }

      onBlur={() => {

        let finalValue =
          localValue

        if (
          type === "number" &&
          localValue !== ""
        ) {

          finalValue =
            Number(localValue)
        }

        onCommit(finalValue)
      }}

      style={{
        width: "100%",
        padding: "6px"
      }}
    />
  )
}

function getValue(
  obj,
  path
) {

  if (!path.length)
    return obj

  let current = obj

  for (const key of path) {

    if (
      current == null
    ) {

      return undefined
    }

    current = current[key]
  }

  return current
}

function resolveRef(
  ref,
  rootSchema
) {

  const refName =
    ref.split("/").pop()

  return rootSchema.$defs[
    refName
  ]
}

function renderSchemaFields({

  schema,

  rootSchema,

  data,

  path,

  onChange

}) {

  // -------------------------
  // Resolve $ref
  // -------------------------

  if (schema.$ref) {

    schema = resolveRef(
      schema.$ref,
      rootSchema
    )
  }

  // -------------------------
  // No properties
  // -------------------------

  if (!schema.properties) {

    return null
  }

  return Object.entries(
    schema.properties
  ).map(([key, definition]) => {

    const currentPath = [
      ...path,
      key
    ]

    const value = getValue(
      data,
      currentPath
    )

    // -------------------------
    // Resolve field $ref
    // -------------------------

    if (definition.$ref) {

      definition = resolveRef(
        definition.$ref,
        rootSchema
      )
    }

    // -------------------------
    // STRING
    // -------------------------

    if (
      definition.type === "string"
    ) {

      return (

        <div
          key={currentPath.join(".")}

          style={{
            marginBottom: "12px"
          }}
        >

          <label>
            {key}
          </label>

          <FieldInput
            type="text"

            value={value}

            onCommit={(v) =>
              onChange(
                currentPath,
                v
              )
            }
          />

        </div>
      )
    }

    // -------------------------
    // NUMBER
    // -------------------------

    if (
      definition.type === "number" ||
      definition.type === "integer"
    ) {

      return (

        <div
          key={currentPath.join(".")}

          style={{
            marginBottom: "12px"
          }}
        >

          <label>
            {key}
          </label>

          <FieldInput
            type="number"

            value={value}

            onCommit={(v) =>
              onChange(
                currentPath,
                v
              )
            }
          />

        </div>
      )
    }

    // -------------------------
    // OBJECT
    // -------------------------

    if (
      definition.type === "object"
    ) {

      return (

        <div
          key={currentPath.join(".")}

          style={{
            marginLeft: "20px",
            paddingLeft: "12px",
            borderLeft:
              "1px solid #ccc",
            marginBottom: "20px"
          }}
        >

          <h4>
            {key}
          </h4>

          {
            renderSchemaFields({

              schema:
                definition,

              rootSchema,

              data,

              path:
                currentPath,

              onChange
            })
          }

        </div>
      )
    }

    // -------------------------
    // ARRAY
    // -------------------------

    if (
      definition.type === "array"
    ) {

      let itemSchema =
        definition.items

      // -----------------------
      // Resolve item $ref
      // -----------------------

      if (
        itemSchema?.$ref
      ) {

        itemSchema =
          resolveRef(
            itemSchema.$ref,
            rootSchema
          )
      }

      const arrayData =
        value || []

      // -----------------------
      // IMPORTANT
      // Show one empty row
      // even if array empty
      // -----------------------

      const rows =
        arrayData.length > 0
          ? arrayData
          : [{}]

      return (

        <div
          key={currentPath.join(".")}

          style={{
            marginLeft: "20px",
            paddingLeft: "12px",
            borderLeft:
              "1px solid #ccc",
            marginBottom: "20px"
          }}
        >

          <h4>
            {key}
          </h4>

          {
            rows.map(
              (item, index) => (

                <div
                  key={index}

                  style={{
                    padding: "10px",
                    marginBottom:
                      "10px",
                    border:
                      "1px solid #ddd"
                  }}
                >

                  <h5>
                    {key} {index + 1}
                  </h5>

                  {
                    renderSchemaFields({

                      schema:
                        itemSchema,

                      rootSchema,

                      data,

                      path: [
                        ...currentPath,
                        index
                      ],

                      onChange
                    })
                  }

                </div>

              )
            )
          }

        </div>
      )
    }

    return null
  })
}

export default function PropertyEditor({

  schema,

  component,

  onChange

}) {

  if (!component) {

    return (
      <div>
        Select Component
      </div>
    )
  }

  if (!schema) {

    return (
      <div>
        Loading Schema...
      </div>
    )
  }

  return (

    <div
      style={{
        padding: "20px"
      }}
    >

      <h3>
        {component.id}
      </h3>

      {
        renderSchemaFields({

          schema,

          rootSchema:
            schema,

          data:
            component.data,

          path: [],

          onChange
        })
      }

    </div>
  )
}
