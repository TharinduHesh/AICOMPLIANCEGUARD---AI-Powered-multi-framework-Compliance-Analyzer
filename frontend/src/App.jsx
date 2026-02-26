import React, { useState, useCallback } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

import { ThemeProvider } from './ThemeContext'
import Layout from './components/Layout'
import Login from './pages/Login'
import Chat from './pages/Chat'
import Dashboard from './pages/Dashboard'
import UploadDocument from './pages/UploadDocument'
import AnalysisResults from './pages/AnalysisResults'
import Frameworks from './pages/Frameworks'
import About from './pages/About'
import History from './pages/History'

function App() {
  const [authed, setAuthed] = useState(() => !!localStorage.getItem('token'))

  const handleAuth = useCallback(() => setAuthed(true), [])
  const handleLogout = useCallback(() => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setAuthed(false)
  }, [])

  // Not logged in → show Login/Register
  if (!authed) {
    return (
      <ThemeProvider>
        <Login onAuth={handleAuth} />
        <ToastContainer position="top-right" autoClose={5000} hideProgressBar={false}
          newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
      </ThemeProvider>
    )
  }

  return (
    <ThemeProvider>
      <Routes>
        {/* Chat is full-screen — no Layout wrapper */}
        <Route path="/" element={<Navigate to="/chat" replace />} />
        <Route path="/chat" element={<Chat onLogout={handleLogout} />} />

        {/* Other pages keep the Layout */}
        <Route path="/dashboard" element={<Layout><Dashboard /></Layout>} />
        <Route path="/upload" element={<Layout><UploadDocument /></Layout>} />
        <Route path="/results/:analysisId" element={<Layout><AnalysisResults /></Layout>} />
        <Route path="/frameworks" element={<Layout><Frameworks /></Layout>} />
        <Route path="/history" element={<Layout><History /></Layout>} />
        <Route path="/about" element={<Layout><About /></Layout>} />
      </Routes>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </ThemeProvider>
  )
}

export default App
