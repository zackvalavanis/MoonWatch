import { useAuth } from "../../auth/AuthContext"

export function Login() {
  const { login } = useAuth()


  return (
    <>
      <button onClick={() => login({ email: 'zackvalavanis@gmail.com', password: "Zackpaul7!" })}>Login</button>
    </>
  )
}