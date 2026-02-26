import React, { useState, useRef, useEffect, useCallback } from 'react'
import ReactMarkdown from 'react-markdown'
import { chatAPI } from '../services/api'
import { useTheme } from '../ThemeContext'

/* ================================================================
   FULL-SCREEN CHATGPT-STYLE COMPLIANCE CHAT  — dark / light theme
   ================================================================ */

/* ── Theme toggle button (sun / moon) ─────────────────────────── */
function ThemeToggle({ isDark, onToggle, t }) {
  return (
    <button
      onClick={onToggle}
      title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
      style={{
        background: 'none', border: 'none', color: t.textMuted,
        cursor: 'pointer', padding: 6, borderRadius: 8,
        display: 'flex', alignItems: 'center', transition: 'color .15s',
      }}
      onMouseEnter={e => e.currentTarget.style.color = t.accent}
      onMouseLeave={e => e.currentTarget.style.color = t.textMuted}
    >
      {isDark ? (
        /* Sun icon */
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
          <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
          <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
      ) : (
        /* Moon icon */
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
      )}
    </button>
  )
}

/* ── Sidebar ──────────────────────────────────────────────────── */
function Sidebar({ conversations, activeId, onSelect, onNew, onDelete, collapsed, user, onLogout, t, isDark, onToggleTheme }) {
  return (
    <div style={{
      width: collapsed ? 0 : 260,
      minWidth: collapsed ? 0 : 260,
      height: '100vh',
      backgroundColor: t.bgSidebar,
      borderRight: `1px solid ${t.border}`,
      display: 'flex',
      flexDirection: 'column',
      transition: 'width 0.25s, min-width 0.25s',
      overflow: 'hidden',
    }}>
      {/* New Chat button */}
      <div style={{ padding: '12px 12px 8px' }}>
        <button
          onClick={onNew}
          style={{
            width: '100%',
            padding: '12px 16px',
            backgroundColor: 'transparent',
            border: `1px solid ${t.borderLight}`,
            borderRadius: 8,
            color: t.text,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            fontSize: 14,
            fontWeight: 500,
            transition: 'background 0.15s',
          }}
          onMouseEnter={e => e.currentTarget.style.backgroundColor = t.bgHover}
          onMouseLeave={e => e.currentTarget.style.backgroundColor = 'transparent'}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          New Chat
        </button>
      </div>

      {/* Conversation list */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '4px 8px' }}>
        {conversations.map(c => (
          <div
            key={c.id}
            onClick={() => onSelect(c.id)}
            style={{
              padding: '10px 12px',
              borderRadius: 8,
              cursor: 'pointer',
              marginBottom: 2,
              backgroundColor: c.id === activeId ? t.bgCard : 'transparent',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              transition: 'background 0.15s',
            }}
            onMouseEnter={e => { if (c.id !== activeId) e.currentTarget.style.backgroundColor = t.bgHover }}
            onMouseLeave={e => { if (c.id !== activeId) e.currentTarget.style.backgroundColor = 'transparent' }}
          >
            <div style={{ overflow: 'hidden', flex: 1 }}>
              <div style={{
                fontSize: 13, color: t.text, whiteSpace: 'nowrap',
                overflow: 'hidden', textOverflow: 'ellipsis',
              }}>
                {c.documentName ? `📄 ${c.documentName}` : c.title || 'New chat'}
              </div>
              <div style={{ fontSize: 11, color: t.textMuted, marginTop: 2 }}>
                {new Date(c.createdAt).toLocaleDateString()}
              </div>
            </div>
            <button
              onClick={(e) => { e.stopPropagation(); onDelete(c.id) }}
              style={{
                background: 'none', border: 'none', color: t.textMuted, cursor: 'pointer',
                padding: 4, borderRadius: 4, fontSize: 14, lineHeight: 1, opacity: 0.5,
              }}
              onMouseEnter={e => e.currentTarget.style.opacity = '1'}
              onMouseLeave={e => e.currentTarget.style.opacity = '0.5'}
            >✕</button>
          </div>
        ))}
      </div>

      {/* Theme toggle row */}
      <div style={{
        padding: '8px 12px', borderTop: `1px solid ${t.border}`,
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      }}>
        <span style={{ color: t.textMuted, fontSize: 12 }}>
          {isDark ? '🌙 Dark' : '☀️ Light'}
        </span>
        <ThemeToggle isDark={isDark} onToggle={onToggleTheme} t={t} />
      </div>

      {/* Bottom — user info + logout */}
      <div style={{
        padding: '12px', borderTop: `1px solid ${t.border}`,
        display: 'flex', alignItems: 'center', gap: 10,
      }}>
        <div style={{
          width: 32, height: 32, borderRadius: '50%',
          backgroundColor: '#1e40af', display: 'flex',
          alignItems: 'center', justifyContent: 'center',
          color: 'white', fontSize: 13, fontWeight: 700, flexShrink: 0,
        }}>
          {(user?.company_id || 'U')[0].toUpperCase()}
        </div>
        <div style={{ flex: 1, overflow: 'hidden' }}>
          <div style={{ color: t.text, fontSize: 13, fontWeight: 500,
            whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {user?.company_name || user?.company_id || 'User'}
          </div>
          <div style={{ color: t.textMuted, fontSize: 11 }}>{user?.company_id}</div>
        </div>
        <button
          onClick={onLogout}
          title="Sign out"
          style={{
            background: 'none', border: 'none', color: t.textMuted,
            cursor: 'pointer', padding: 6, borderRadius: 8,
            display: 'flex', alignItems: 'center', transition: 'color .15s',
          }}
          onMouseEnter={e => e.currentTarget.style.color = '#ef4444'}
          onMouseLeave={e => e.currentTarget.style.color = t.textMuted}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
        </button>
      </div>
    </div>
  )
}

/* ── Message Bubble ───────────────────────────────────────────── */
function MessageBubble({ role, content, documentName, t }) {
  const isUser = role === 'user'

  return (
    <div style={{
      display: 'flex', justifyContent: 'center',
      backgroundColor: isUser ? 'transparent' : t.bgBubbleAI,
      padding: '24px 0',
    }}>
      <div style={{
        maxWidth: 760, width: '100%', display: 'flex', gap: 16, padding: '0 24px',
      }}>
        {/* Avatar */}
        <div style={{
          width: 36, height: 36, borderRadius: '50%', flexShrink: 0,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 14, fontWeight: 700, color: 'white',
          background: isUser
            ? `linear-gradient(135deg, ${t.userGrad1}, ${t.userGrad2})`
            : `linear-gradient(135deg, ${t.accent}, ${t.accentDark})`,
        }}>
          {isUser ? 'U' : 'AI'}
        </div>

        {/* Content */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{
            fontSize: 13, fontWeight: 600, marginBottom: 6,
            color: isUser ? t.userLabel : t.accentText,
          }}>
            {isUser ? 'You' : 'AI Compliance Assistant'}
          </div>

          {documentName && (
            <div style={{
              display: 'inline-flex', alignItems: 'center', gap: 6,
              padding: '6px 12px', backgroundColor: t.bgCard,
              borderRadius: 8, border: `1px solid ${t.borderLight}`,
              marginBottom: 8, fontSize: 13, color: t.textSecondary,
            }}>
              📎 {documentName}
            </div>
          )}

          <div className="chat-md" style={{ color: t.text, fontSize: 15, lineHeight: 1.7 }}>
            <ReactMarkdown>{content}</ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  )
}

/* ── Typing dots ──────────────────────────────────────────────── */
function TypingIndicator({ t }) {
  return (
    <div style={{
      display: 'flex', justifyContent: 'center',
      backgroundColor: t.bgBubbleAI, padding: '24px 0',
    }}>
      <div style={{
        maxWidth: 760, width: '100%', display: 'flex', gap: 16, padding: '0 24px',
      }}>
        <div style={{
          width: 36, height: 36, borderRadius: '50%', flexShrink: 0,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          background: `linear-gradient(135deg, ${t.accent}, ${t.accentDark})`,
          color: 'white', fontWeight: 700, fontSize: 14,
        }}>AI</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 5, paddingTop: 10 }}>
          {[0, 1, 2].map(i => (
            <div key={i} style={{
              width: 8, height: 8, borderRadius: '50%', backgroundColor: t.accentLight,
              animation: 'chatPulse 1.2s infinite',
              animationDelay: `${i * 0.2}s`,
            }} />
          ))}
        </div>
      </div>
    </div>
  )
}

/* ── Welcome screen (centered like ChatGPT) ───────────────────── */
function WelcomeScreen({ onSend, t }) {
  const suggestions = [
    { icon: '📋', title: 'What is ISO 27001?', desc: 'Information security standards' },
    { icon: '🛡️', title: 'Explain the CIA triad', desc: 'Confidentiality, Integrity, Availability' },
    { icon: '📜', title: 'What is GDPR?', desc: 'Data privacy regulations' },
    { icon: '🔍', title: 'How does NIST CSF work?', desc: 'Cybersecurity framework overview' },
  ]

  return (
    <div style={{
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      justifyContent: 'center', flex: 1, padding: 40,
    }}>
      <div style={{
        width: 72, height: 72, borderRadius: 16,
        background: `linear-gradient(135deg, ${t.accent}, ${t.accentDark})`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        marginBottom: 24, fontSize: 34,
      }}>🔐</div>

      <h1 style={{
        fontSize: 30, fontWeight: 700, color: t.textHeading,
        marginBottom: 8, textAlign: 'center',
      }}>AI Compliance Assistant</h1>

      <p style={{
        color: t.textSecondary, fontSize: 16, textAlign: 'center',
        maxWidth: 520, lineHeight: 1.6, marginBottom: 40,
      }}>
        Upload a compliance document and I'll analyze it against ISO 27001, ISO 9001,
        NIST CSF, or GDPR. I'll find gaps, weak policies, and give you actionable improvements.
      </p>

      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)',
        gap: 12, maxWidth: 560, width: '100%',
      }}>
        {suggestions.map(s => (
          <button
            key={s.title}
            onClick={() => onSend(s.title)}
            style={{
              padding: 16, backgroundColor: t.bgWelcome,
              border: `1px solid ${t.borderLight}`, borderRadius: 12,
              cursor: 'pointer', textAlign: 'left',
              transition: 'all 0.15s', color: t.text,
            }}
            onMouseEnter={e => {
              e.currentTarget.style.borderColor = t.accentLight
              e.currentTarget.style.backgroundColor = t.bgHover
            }}
            onMouseLeave={e => {
              e.currentTarget.style.borderColor = t.borderLight
              e.currentTarget.style.backgroundColor = t.bgWelcome
            }}
          >
            <div style={{ fontSize: 22, marginBottom: 6 }}>{s.icon}</div>
            <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 4 }}>{s.title}</div>
            <div style={{ fontSize: 12, color: t.textMuted }}>{s.desc}</div>
          </button>
        ))}
      </div>
    </div>
  )
}

/* ── File preview chip ────────────────────────────────────────── */
function FilePreview({ file, onRemove, t }) {
  return (
    <div style={{
      display: 'inline-flex', alignItems: 'center', gap: 8,
      padding: '8px 14px', backgroundColor: t.bgCard,
      border: `1px solid ${t.borderLight}`, borderRadius: 10,
      marginBottom: 8, fontSize: 13, color: t.textSecondary,
    }}>
      📄 <span style={{ color: t.text, fontWeight: 500 }}>{file.name}</span>
      <span style={{ fontSize: 11, color: t.textMuted }}>({(file.size / 1024).toFixed(1)} KB)</span>
      <button onClick={onRemove} style={{
        background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer',
        padding: '0 2px', fontSize: 16, lineHeight: 1,
      }}>✕</button>
    </div>
  )
}

/* ── Quick chips ──────────────────────────────────────────────── */
function ActionChips({ onSend, hasDoc, t }) {
  const docChips = [
    '🔍 Full compliance analysis',
    '📋 Check against ISO 27001',
    '❌ What controls are missing?',
    '⚠️ Show weak policies',
    '💡 How can I improve?',
    '🛡️ CIA triad analysis',
  ]
  const generalChips = [
    'What is ISO 27001?',
    'Explain CIA triad',
    'What is GDPR?',
    'NIST CSF overview',
  ]
  const chips = hasDoc ? docChips : generalChips

  return (
    <div style={{
      display: 'flex', flexWrap: 'wrap', gap: 8,
      justifyContent: 'center', padding: '0 24px 8px',
    }}>
      {chips.map(label => (
        <button
          key={label}
          onClick={() => onSend(label)}
          style={{
            padding: '6px 14px', borderRadius: 20,
            border: `1px solid ${t.borderLight}`, backgroundColor: 'transparent',
            color: t.textSecondary, fontSize: 13, cursor: 'pointer',
            transition: 'all 0.15s',
          }}
          onMouseEnter={e => {
            e.currentTarget.style.borderColor = t.accentLight
            e.currentTarget.style.color = t.text
          }}
          onMouseLeave={e => {
            e.currentTarget.style.borderColor = t.borderLight
            e.currentTarget.style.color = t.textSecondary
          }}
        >{label}</button>
      ))}
    </div>
  )
}

/* ================================================================
   MAIN CHAT COMPONENT
   ================================================================ */
export default function Chat({ onLogout }) {
  const { theme: t, isDark, toggle: toggleTheme } = useTheme()

  const [conversations, setConversations] = useState([])
  const [activeConvId, setActiveConvId] = useState(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [documentName, setDocumentName] = useState(null)
  const [pendingFile, setPendingFile] = useState(null)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [user] = useState(() => {
    try { return JSON.parse(localStorage.getItem('user')) } catch { return null }
  })
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)
  const textareaRef = useRef(null)

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  useEffect(() => { scrollToBottom() }, [messages, loading])

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + 'px'
    }
  }, [input])

  // Create initial conversation on mount
  useEffect(() => { handleNewChat() }, [])

  /* ── Conversation management ─────────── */
  const handleNewChat = async () => {
    try {
      const data = await chatAPI.newConversation()
      const c = { id: data.conversation_id, title: 'New chat', documentName: null, createdAt: data.timestamp || new Date().toISOString() }
      setConversations(prev => [c, ...prev])
      setActiveConvId(data.conversation_id)
      setMessages([])
      setDocumentName(null)
      setPendingFile(null)
    } catch {
      const id = `local_${Date.now()}`
      setConversations(prev => [{ id, title: 'New chat', documentName: null, createdAt: new Date().toISOString() }, ...prev])
      setActiveConvId(id)
      setMessages([])
      setDocumentName(null)
      setPendingFile(null)
    }
  }

  const handleSelectConversation = async (id) => {
    setActiveConvId(id)
    try {
      const data = await chatAPI.getConversation(id)
      setMessages(data.messages || [])
      setDocumentName(data.document_name || null)
    } catch { setMessages([]) }
  }

  const handleDeleteConversation = async (id) => {
    try { await chatAPI.deleteConversation(id) } catch {}
    setConversations(prev => prev.filter(c => c.id !== id))
    if (activeConvId === id) {
      setActiveConvId(null)
      setMessages([])
      setDocumentName(null)
    }
  }

  /* ── Send message ───────────────────── */
  const sendMessage = useCallback(async (text) => {
    const msg = (text || input).trim()
    if (!msg && !pendingFile) return
    if (loading) return
    setInput('')

    // file + message → upload-and-ask
    if (pendingFile) {
      const file = pendingFile
      setPendingFile(null)
      setMessages(prev => [...prev, { role: 'user', content: msg || `📎 Uploaded: **${file.name}**`, documentName: file.name, timestamp: new Date().toISOString() }])
      setLoading(true)
      try {
        const data = await chatAPI.uploadAndAsk(activeConvId, file, msg || 'Analyze this document for compliance', 'iso27001')
        setActiveConvId(data.conversation_id)
        setDocumentName(data.document_name)
        setConversations(prev => prev.map(c => c.id === activeConvId ? { ...c, documentName: data.document_name, title: data.document_name } : c))
        setMessages(prev => [...prev, { role: 'assistant', content: data.message, timestamp: data.timestamp }])
      } catch {
        setMessages(prev => [...prev, { role: 'assistant', content: '⚠️ Failed to upload. Make sure backend is running at http://localhost:8000', timestamp: new Date().toISOString() }])
      } finally { setLoading(false) }
      return
    }

    // Normal text
    setMessages(prev => [...prev, { role: 'user', content: msg, timestamp: new Date().toISOString() }])
    setLoading(true)
    if (messages.length === 0) {
      setConversations(prev => prev.map(c => c.id === activeConvId ? { ...c, title: msg.slice(0, 40) } : c))
    }
    try {
      const data = await chatAPI.sendMessage(activeConvId, msg)
      setActiveConvId(data.conversation_id)
      setMessages(prev => [...prev, { role: 'assistant', content: data.message, timestamp: data.timestamp }])
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: '⚠️ Could not reach backend. Make sure it\'s running at http://localhost:8000', timestamp: new Date().toISOString() }])
    } finally { setLoading(false) }
  }, [input, loading, activeConvId, pendingFile, messages.length])

  /* ── File handling ──────────────────── */
  const handleFileSelect = (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    const ext = file.name.split('.').pop().toLowerCase()
    if (!['pdf', 'docx'].includes(ext)) {
      setMessages(prev => [...prev, { role: 'assistant', content: '❌ Only **PDF** and **DOCX** files are supported.', timestamp: new Date().toISOString() }])
      return
    }
    if (file.size > 10 * 1024 * 1024) {
      setMessages(prev => [...prev, { role: 'assistant', content: '❌ File too large. Max **10 MB**.', timestamp: new Date().toISOString() }])
      return
    }
    setPendingFile(file)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  const handleUploadOnly = async (file) => {
    setMessages(prev => [...prev, { role: 'user', content: `📎 Uploaded: **${file.name}**`, documentName: file.name, timestamp: new Date().toISOString() }])
    setLoading(true)
    try {
      const data = await chatAPI.uploadDocument(activeConvId, file)
      setActiveConvId(data.conversation_id)
      setDocumentName(data.document_name)
      setConversations(prev => prev.map(c => c.id === activeConvId ? { ...c, documentName: data.document_name, title: data.document_name } : c))
      setMessages(prev => [...prev, { role: 'assistant', content: data.message, timestamp: data.timestamp }])
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: '⚠️ Upload failed. Backend may be offline.', timestamp: new Date().toISOString() }])
    } finally { setLoading(false) }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      if (pendingFile && !input.trim()) {
        const f = pendingFile; setPendingFile(null); handleUploadOnly(f)
      } else {
        sendMessage()
      }
    }
  }

  const isEmpty = messages.length === 0

  /* ══════════════════════════════════════════════════════════════ */
  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', backgroundColor: t.bg, overflow: 'hidden', position: 'fixed', top: 0, left: 0, zIndex: 9999 }}>

      {/* Dynamic styles */}
      <style>{`
        @keyframes chatPulse {
          0%, 80%, 100% { opacity: .3; transform: scale(.8); }
          40% { opacity: 1; transform: scale(1.1); }
        }
        .chat-md h2 { font-size: 1.15rem; font-weight: 700; margin: 12px 0 6px; color: ${t.textHeading}; }
        .chat-md h3 { font-size: 1.05rem; font-weight: 600; margin: 10px 0 4px; color: ${t.text}; }
        .chat-md p  { margin: 0 0 8px; }
        .chat-md ul, .chat-md ol { margin: 4px 0 8px; padding-left: 20px; }
        .chat-md li { margin-bottom: 3px; }
        .chat-md strong { color: ${t.textHeading}; }
        .chat-md em { color: ${t.textSecondary}; }
        .chat-md blockquote {
          border-left: 3px solid ${t.accentLight}; padding-left: 12px;
          margin: 8px 0; color: ${t.textSecondary}; font-style: italic;
        }
        .chat-md code {
          background: ${isDark ? 'rgba(255,255,255,.08)' : 'rgba(0,0,0,.06)'}; padding: 1px 5px;
          border-radius: 4px; font-size: .88em;
        }
        .chat-md hr { border: none; border-top: 1px solid ${t.borderLight}; margin: 12px 0; }
        .chat-scroll::-webkit-scrollbar { width: 6px; }
        .chat-scroll::-webkit-scrollbar-track { background: transparent; }
        .chat-scroll::-webkit-scrollbar-thumb { background: ${t.scrollThumb}; border-radius: 3px; }
        .chat-ta::-webkit-scrollbar { width: 4px; }
        .chat-ta::-webkit-scrollbar-thumb { background: ${t.scrollThumb}; border-radius: 2px; }
      `}</style>

      {/* ── Sidebar ───────────────────────── */}
      <Sidebar
        conversations={conversations}
        activeId={activeConvId}
        onSelect={handleSelectConversation}
        onNew={handleNewChat}
        onDelete={handleDeleteConversation}
        collapsed={sidebarCollapsed}
        user={user}
        onLogout={onLogout}
        t={t}
        isDark={isDark}
        onToggleTheme={toggleTheme}
      />

      {/* ── Main area ─────────────────────── */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', height: '100vh' }}>

        {/* Top bar */}
        <div style={{
          display: 'flex', alignItems: 'center', padding: '10px 16px',
          borderBottom: `1px solid ${t.border}`, backgroundColor: t.bg,
          zIndex: 10, gap: 12, flexShrink: 0,
        }}>
          <button
            onClick={() => setSidebarCollapsed(p => !p)}
            style={{
              background: 'none', border: 'none', color: t.textSecondary,
              cursor: 'pointer', padding: 6, borderRadius: 6, display: 'flex',
            }}
            onMouseEnter={e => e.currentTarget.style.backgroundColor = t.bgCard}
            onMouseLeave={e => e.currentTarget.style.backgroundColor = 'transparent'}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
          </button>
          <div style={{ flex: 1 }}>
            <span style={{ color: t.text, fontWeight: 600, fontSize: 15 }}>AI Compliance Assistant</span>
            {documentName && <span style={{ color: t.accentLight, fontSize: 13, marginLeft: 12 }}>📄 {documentName}</span>}
          </div>

          {/* Theme toggle in top bar (visible when sidebar collapsed) */}
          {sidebarCollapsed && (
            <ThemeToggle isDark={isDark} onToggle={toggleTheme} t={t} />
          )}

          <div style={{
            padding: '4px 10px', borderRadius: 12,
            backgroundColor: t.accentBg, color: t.accentText,
            fontSize: 11, fontWeight: 600,
          }}>● Online</div>
        </div>

        {/* Messages */}
        <div className="chat-scroll" style={{
          flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column',
        }}>
          {isEmpty ? (
            <WelcomeScreen onSend={sendMessage} t={t} />
          ) : (
            <>
              {messages.map((m, i) => (
                <MessageBubble key={i} role={m.role} content={m.content} documentName={m.documentName} t={t} />
              ))}
              {loading && <TypingIndicator t={t} />}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Quick chips */}
        {!isEmpty && !loading && messages.length <= 4 && (
          <ActionChips onSend={sendMessage} hasDoc={!!documentName} t={t} />
        )}

        {/* ── Input ───────────────────────── */}
        <div style={{ padding: '12px 24px 20px', display: 'flex', justifyContent: 'center', flexShrink: 0 }}>
          <div style={{ maxWidth: 760, width: '100%' }}>

            {/* Pending file */}
            {pendingFile && <FilePreview file={pendingFile} onRemove={() => setPendingFile(null)} t={t} />}

            <div style={{
              display: 'flex', alignItems: 'flex-end', gap: 0,
              backgroundColor: t.bgInput, borderRadius: 16,
              border: `1px solid ${t.borderLight}`, padding: '8px 8px 8px 16px',
            }}>
              {/* Attach */}
              <input ref={fileInputRef} type="file" accept=".pdf,.docx" style={{ display: 'none' }} onChange={handleFileSelect} />
              <button
                onClick={() => fileInputRef.current?.click()}
                disabled={loading}
                title="Upload PDF or DOCX"
                style={{
                  background: 'none', border: 'none', color: t.textMuted,
                  cursor: loading ? 'not-allowed' : 'pointer',
                  padding: 6, borderRadius: 8, display: 'flex',
                  alignItems: 'center', flexShrink: 0, marginBottom: 2,
                  transition: 'color .15s',
                }}
                onMouseEnter={e => { if (!loading) e.currentTarget.style.color = t.text }}
                onMouseLeave={e => e.currentTarget.style.color = t.textMuted}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
                </svg>
              </button>

              {/* Textarea */}
              <textarea
                ref={textareaRef}
                className="chat-ta"
                rows={1}
                placeholder={documentName ? 'Ask about compliance, missing controls, improvements...' : 'Message AI Compliance Assistant...'}
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading}
                style={{
                  flex: 1, border: 'none', outline: 'none',
                  backgroundColor: 'transparent', color: t.text,
                  fontSize: 15, resize: 'none', padding: '8px',
                  maxHeight: 200, lineHeight: 1.5, fontFamily: 'inherit',
                }}
              />

              {/* Send */}
              <button
                onClick={() => {
                  if (pendingFile && !input.trim()) { const f = pendingFile; setPendingFile(null); handleUploadOnly(f) }
                  else sendMessage()
                }}
                disabled={loading || (!input.trim() && !pendingFile)}
                style={{
                  width: 36, height: 36, borderRadius: '50%', border: 'none',
                  backgroundColor: (input.trim() || pendingFile) && !loading ? t.accent : t.btnDisabled,
                  color: (input.trim() || pendingFile) && !loading ? 'white' : t.btnDisabledText,
                  cursor: (input.trim() || pendingFile) && !loading ? 'pointer' : 'not-allowed',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  flexShrink: 0, transition: 'all .15s', marginBottom: 2,
                }}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                </svg>
              </button>
            </div>

            <div style={{ textAlign: 'center', color: t.textDimmed, fontSize: 11, marginTop: 8 }}>
              Upload PDF/DOCX compliance documents • Supports ISO 27001, ISO 9001, NIST, GDPR
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
