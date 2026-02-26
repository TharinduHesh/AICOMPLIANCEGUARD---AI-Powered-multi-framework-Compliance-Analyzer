import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  AppBar,
  Box,
  Toolbar,
  IconButton,
  Typography,
  Menu,
  Container,
  Button,
  MenuItem,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  useMediaQuery,
  useTheme,
} from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'
import SecurityIcon from '@mui/icons-material/Security'
import ChatIcon from '@mui/icons-material/Chat'
import DashboardIcon from '@mui/icons-material/Dashboard'
import UploadFileIcon from '@mui/icons-material/UploadFile'
import AssessmentIcon from '@mui/icons-material/Assessment'
import HistoryIcon from '@mui/icons-material/History'
import InfoIcon from '@mui/icons-material/Info'

const pages = [
  { name: 'AI Chat', path: '/chat', icon: <ChatIcon /> },
  { name: 'Dashboard', path: '/dashboard', icon: <DashboardIcon /> },
  { name: 'Upload Document', path: '/upload', icon: <UploadFileIcon /> },
  { name: 'Frameworks', path: '/frameworks', icon: <AssessmentIcon /> },
  { name: 'History', path: '/history', icon: <HistoryIcon /> },
  { name: 'About', path: '/about', icon: <InfoIcon /> },
]

function Layout({ children }) {
  const [mobileOpen, setMobileOpen] = useState(false)
  const location = useLocation()
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen)
  }

  const drawer = (
    <Box onClick={handleDrawerToggle} sx={{ textAlign: 'center' }}>
      <Typography variant="h6" sx={{ my: 2, color: 'white' }}>
        🔐 AIComplianceGuard
      </Typography>
      <Divider sx={{ borderColor: '#334155' }} />
      <List>
        {pages.map((page) => (
          <ListItem
            key={page.name}
            component={Link}
            to={page.path}
            selected={location.pathname === page.path}
            sx={{
              color: 'white',
              '&.Mui-selected': {
                backgroundColor: '#1e3a8a',
                color: 'white',
                '& .MuiListItemIcon-root': {
                  color: 'white',
                },
              },
              '&:hover': {
                backgroundColor: '#334155',
              },
            }}
          >
            <ListItemIcon sx={{ color: 'white' }}>{page.icon}</ListItemIcon>
            <ListItemText primary={page.name} />
          </ListItem>
        ))}
      </List>
    </Box>
  )

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static" elevation={2}>
        <Container maxWidth="xl">
          <Toolbar disableGutters>
            {isMobile && (
              <IconButton
                color="inherit"
                aria-label="open drawer"
                edge="start"
                onClick={handleDrawerToggle}
                sx={{ mr: 2 }}
              >
                <MenuIcon />
              </IconButton>
            )}

            <SecurityIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} />
            <Typography
              variant="h6"
              noWrap
              component={Link}
              to="/"
              sx={{
                mr: 2,
                display: { xs: 'none', md: 'flex' },
                fontWeight: 700,
                color: 'inherit',
                textDecoration: 'none',
              }}
            >
              AIComplianceGuard
            </Typography>

            <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
              {pages.map((page) => (
                <Button
                  key={page.name}
                  component={Link}
                  to={page.path}
                  sx={{
                    my: 2,
                    color: 'white',
                    display: 'block',
                    backgroundColor:
                      location.pathname === page.path ? 'rgba(255, 255, 255, 0.15)' : 'transparent',
                    '&:hover': {
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    },
                  }}
                >
                  {page.name}
                </Button>
              ))}
            </Box>
          </Toolbar>
        </Container>
      </AppBar>

      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true,
        }}
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': { 
            boxSizing: 'border-box', 
            width: 240,
            backgroundColor: '#1e293b',
            color: '#ffffff',
          },
        }}
      >
        {drawer}
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, py: 3, backgroundColor: 'background.default' }}>
        <Container maxWidth="xl">{children}</Container>
      </Box>

      <Box
        component="footer"
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
          backgroundColor: '#1e293b',
          borderTop: '1px solid #334155',
        }}
      >
        <Container maxWidth="xl">
          <Typography variant="body2" color="text.secondary" align="center">
            © 2026 AIComplianceGuard - Secure AI-Powered Compliance Validation Platform
          </Typography>
          <Typography variant="caption" color="text.secondary" align="center" display="block">
            Built with ❤️ for secure compliance automation
          </Typography>
        </Container>
      </Box>
    </Box>
  )
}

export default Layout
