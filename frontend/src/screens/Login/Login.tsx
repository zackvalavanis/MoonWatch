import { useAuth } from "../../auth/AuthContext"

export function Login() {
  const { login, logout, user } = useAuth()

  console.log(user)


  return (
    <>
      <button onClick={() => login({ email: 'zackvalavanis@gmail.com', password: "Zackpaul7!" })}>Login</button>
      <button onClick={() => logout()}>Logout</button>
    </>
  )
}