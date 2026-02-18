import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { SnackbarProvider } from 'notistack';
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login/Login';
import VenuesPage from './pages/Venues';
import PortalTemplatesPage from './pages/PortalTemplates';
import ReportsPage from './pages/Reports';
import NasDevicesPage from './pages/NasDevices';
import UserProfilesPage from './pages/UserProfiles';
import UsersPage from './pages/Users';
import BannersPage from './pages/Banners';
import Dashboard from './pages/Dashboard';
import DataAudit from './pages/DataAudit';
import WireGuardPeers from './pages/WireGuardPeers';
import SmsProvidersPage from './pages/SmsProviders';
import TelegramAuthPage from './pages/TelegramAuthPage';
import SettingsPage from './pages/Settings';
import NasLogs from './pages/NasLogs'; // будет создан позже
import CrmProvidersPage from './pages/CrmProviders';
import SocialActionsPage from './pages/SocialActions';
import RadiusAttributesPage from './pages/RadiusAttributes';
import TariffsPage from './pages/Tariffs';

// внутри <Routes> добавьте:


// внутри <Routes> добавьте:


// Внутри <Routes> добавьте:


function App() {
  return (
    <BrowserRouter>
      <SnackbarProvider maxSnack={3} anchorOrigin={{ vertical: 'top', horizontal: 'right' }}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/telegram-auth" element={<TelegramAuthPage />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/venues" replace />} />
            <Route path="venues" element={<VenuesPage />} />
            <Route path="data-audit" element={<DataAudit />} />
            <Route path="sms-providers" element={<SmsProvidersPage />} />
            <Route path="wireguard-peers" element={<WireGuardPeers />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="nas-devices" element={<NasDevicesPage />} />
            <Route path="nas-logs" element={<NasLogs />} />
            <Route path="banners" element={<BannersPage />} />
            <Route path="/social-actions" element={<SocialActionsPage />} />
            <Route path="user-profiles" element={<UserProfilesPage />} />
            <Route path="users" element={<UsersPage />} />
            <Route path="portal-templates" element={<PortalTemplatesPage />} />
            <Route path="reports" element={<ReportsPage />} />
            <Route path="settings" element={<SettingsPage />} />
            <Route path="/crm-providers" element={<CrmProvidersPage />} />
            <Route path="/radius-attributes" element={<RadiusAttributesPage />} />
            <Route path="/tariffs" element={<TariffsPage />} />
          </Route>
        </Routes>
      </SnackbarProvider>
    </BrowserRouter>
  );
}

export default App;