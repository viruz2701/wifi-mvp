import { Tabs, Tab, Box } from '@mui/material';
import { useState } from 'react';
import ActivityReport from './ActivityReport';

export default function ReportsPage() {
  const [tab, setTab] = useState(0);

  return (
    <Box>
      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 2 }}>
        <Tab label="Активность" />
        <Tab label="Топ пользователей" />
        <Tab label="Устройства" />
        <Tab label="SMS" />
      </Tabs>
      <Box hidden={tab !== 0}>
        <ActivityReport />
      </Box>
      <Box hidden={tab !== 1}>
        <div>Топ пользователей – в разработке</div>
      </Box>
      <Box hidden={tab !== 2}>
        <div>Устройства – в разработке</div>
      </Box>
      <Box hidden={tab !== 3}>
        <div>SMS – в разработке</div>
      </Box>
    </Box>
  );
}
