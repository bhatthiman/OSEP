export default function ProjectStructure({
  components,
  selectedId,
  onSelect
}) {

  return (

    <div>

      <h3>
        Project Structure
      </h3>

      {
        components.map(component => (

          <div
            key={component.id}

            onClick={() =>
              onSelect(component)
            }

            style={{
              padding: "8px",
              cursor: "pointer",
              background:
                selectedId === component.id
                  ? "#ddd"
                  : "transparent"
            }}
          >

            {component.id}

          </div>

        ))
      }

    </div>
  )
}
