import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login/Login';
import VenuesPage from './pages/Venues';
import PortalTemplatesPage from './pages/PortalTemplates';
import ReportsPage from './pages/Reports';

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
          <Route path="portal-templates" element={<PortalTemplatesPage />} />
          <Route path="reports" element={<ReportsPage />} />
          {/* Добавьте остальные маршруты по аналогии */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
