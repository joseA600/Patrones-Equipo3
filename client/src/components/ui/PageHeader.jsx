export function PageHeader({ eyebrow, title, description }) {
  return (
    <section className="page-header">
      <span className="eyebrow">{eyebrow}</span>
      <h2>{title}</h2>
      <p>{description}</p>
    </section>
  )
}
