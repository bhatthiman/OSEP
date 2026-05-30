export default function ComponentLibrary({
  componentTypes,
  onAdd
}) {

  return (

    <div
      style={{
        padding: "10px",
        borderRight:
          "1px solid #ccc"
      }}
    >

      <h3>
        Component Library
      </h3>

      {
        componentTypes.map(type => (

          <button
            key={type}

            onClick={() =>
              onAdd(type)
            }

            style={{
              width: "100%",
              marginBottom: "10px"
            }}
          >

            Add {type}

          </button>

        ))
      }

    </div>
  )
}
