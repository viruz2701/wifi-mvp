import { Box, CssBaseline, AppBar, Toolbar, Typography, Drawer, List, ListItem, ListItemIcon, ListItemText, IconButton } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { useState } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import DashboardIcon from '@mui/icons-material/Dashboard';
import LocationCityIcon from '@mui/icons-material/LocationCity';
import RouterIcon from '@mui/icons-material/Router';
import WebIcon from '@mui/icons-material/Web';
import ImageIcon from '@mui/icons-material/Image';
import PeopleIcon from '@mui/icons-material/People';
import AssessmentIcon from '@mui/icons-material/Assessment';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import LogoutIcon from '@mui/icons-material/Logout';
import { useAuth } from '@/hooks/useAuth';
import VpnKeyIcon from '@mui/icons-material/VpnKey';

const drawerWidth = 240;

export default function Layout() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleDrawerToggle = () => setMobileOpen(!mobileOpen);

 

const menuItems = [
  { text: 'Площадки', icon: <LocationCityIcon />, path: '/venues', roles: ['admin', 'venue_owner'] },
  { text: 'NAS-устройства', icon: <RouterIcon />, path: '/nas-devices', roles: ['admin', 'venue_owner'] },
  { text: 'Шаблоны портала', icon: <WebIcon />, path: '/portal-templates', roles: ['admin'] },
  { text: 'Баннеры', icon: <ImageIcon />, path: '/banners', roles: ['admin', 'marketing'] },
  { text: 'Пользователи Wi-Fi', icon: <PeopleIcon />, path: '/user-profiles', roles: ['admin', 'venue_owner', 'support'] },
  { text: 'Отчёты', icon: <AssessmentIcon />, path: '/reports', roles: ['admin', 'marketing'] },
  { text: 'Администраторы', icon: <AdminPanelSettingsIcon />, path: '/users', roles: ['admin'] },
  { text: 'WireGuard Peers', icon: <VpnKeyIcon />, path: '/wireguard-peers', roles: ['admin'] },   // новый пункт
];

  const drawer = (
    <div>
      <Toolbar>
        <Typography variant="h6" noWrap>
          WiFi Auth
        </Typography>
      </Toolbar>
      <List>
        {menuItems.map((item) => {
          if (item.roles && !item.roles.includes(user?.role || '') && !user?.is_superuser) return null;
          return (
            <ListItem button key={item.text} onClick={() => navigate(item.path)}>
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItem>
          );
        })}
        <ListItem button onClick={logout}>
          <ListItemIcon><LogoutIcon /></ListItemIcon>
          <ListItemText primary="Выход" />
        </ListItem>
      </List>
    </div>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <IconButton color="inherit" edge="start" onClick={handleDrawerToggle} sx={{ mr: 2, display: { sm: 'none' } }}>
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap>
            Административная панель
          </Typography>
        </Toolbar>
      </AppBar>
      <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{ display: { xs: 'block', sm: 'none' }, '& .MuiDrawer-paper': { width: drawerWidth } }}
        >
          {drawer}
        </Drawer>
        <Drawer variant="permanent" sx={{ display: { xs: 'none', sm: 'block' }, '& .MuiDrawer-paper': { width: drawerWidth } }} open>
          {drawer}
        </Drawer>
      </Box>
      <Box component="main" sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}>
        <Toolbar />
        <Outlet />
      </Box>
    </Box>
  );
}
