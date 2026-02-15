import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
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




function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
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
          


          <Route path="wireguard-peers" element={<WireGuardPeers />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="nas-devices" element={<NasDevicesPage />} />
          <Route path="banners" element={<BannersPage />} />
          <Route path="user-profiles" element={<UserProfilesPage />} />
          <Route path="users" element={<UsersPage />} />
          <Route path="portal-templates" element={<PortalTemplatesPage />} />
          <Route path="reports" element={<ReportsPage />} />
          {/* Добавьте остальные маршруты по аналогии */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
