// One feedback from GET /feedback:
// { id, subject, message, rating, created_at }
function Dashboard({ feedback, onLogout }) {
  return (
    <section>
      <h2>My feedback</h2>
      <button onClick={onLogout}>Logout</button>

      {feedback.length === 0 ? (
        <p>You have not submitted any feedback yet.</p>
      ) : (
        <ul>
          {feedback.map((item) => (
            <li key={item.id}>
              <h3>{item.subject}</h3>
              <p>{item.message}</p>
              <p>Rating: {item.rating}</p>
              <p>Date: {new Date(item.created_at).toLocaleString()}</p>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default Dashboard;
