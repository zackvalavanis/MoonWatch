
import { useAuth } from "../../auth/useAuth"
import "./HomePage.css"

export function HomePage() {
  const { user } = useAuth();
  const firstName = user?.first_name ?? "";
  const firstLetter = firstName ? firstName[0].toUpperCase() : "";

  return (
    <div className="homepage">
      <section>
        {user && (
          <h1>
            Welcome {firstLetter}
            {firstName.slice(1)}
          </h1>
        )}
      </section>

      <section>
        <h1>Section 2</h1>
      </section>

      <section>
        <h1>Section 3</h1>
      </section>
    </div>
  );
}