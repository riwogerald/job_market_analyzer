@@ .. @@
 import React from 'react';
 import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
 import { QueryClient, QueryClientProvider } from 'react-query';
 import { ThemeProvider, createTheme } from '@mui/material/styles';
-import CssBaseline from '@mui/material/CssBaseline';
-import { AppBar, Toolbar, Typography, Container } from '@mui/material';
+import CssBaseline from '@mui/material/CssBaseline';
+import { AppBar, Toolbar, Typography, Container, Button, Box } from '@mui/material';
+import { Link, useLocation } from 'react-router-dom';
+import { Dashboard, Work, Analytics } from '@mui/icons-material';

 import Dashboard from './components/Dashboard/Dashboard';
 import JobList from './components/Jobs/JobList';
 import JobDetail from './components/Jobs/JobDetail';
 import Analytics from './components/Analytics/Analytics';

+const NavigationBar: React.FC = () => {
+  const location = useLocation();
+  
+  const navItems = [
+    { path: '/', label: 'Dashboard', icon: <Dashboard /> },
+    { path: '/jobs', label: 'Jobs', icon: <Work /> },
+    { path: '/analytics', label: 'Analytics', icon: <Analytics /> },
+  ];
+
+  return (
+    <AppBar position="static">
+      <Toolbar>
+        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
+          Kenya Job Market Analyzer
+        </Typography>
+        <Box sx={{ display: 'flex', gap: 1 }}>
+          {navItems.map((item) => (
+            <Button
+              key={item.path}
+              component={Link}
+              to={item.path}
+              color="inherit"
+              startIcon={item.icon}
+              variant={location.pathname === item.path ? 'outlined' : 'text'}
+              sx={{ 
+                color: 'white',
+                borderColor: location.pathname === item.path ? 'white' : 'transparent'
+              }}
+            >
+              {item.label}
+            </Button>
+          ))}
+        </Box>
+      </Toolbar>
+    </AppBar>
+  );
+};
+
 const theme = createTheme({
   palette: {
     primary: {
       main: '#1976d2',
     },
     secondary: {
       main: '#dc004e',
     },
   },
 });

 const queryClient = new QueryClient({
   defaultOptions: {
     queries: {
       refetchOnWindowFocus: false,
       retry: 1,
       staleTime: 5 * 60 * 1000, // 5 minutes
     },
   },
 });

 function App() {
   return (
     <QueryClientProvider client={queryClient}>
       <ThemeProvider theme={theme}>
         <CssBaseline />
         <Router>
-          <AppBar position="static">
-            <Toolbar>
-              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
-                Kenya Job Market Analyzer
-              </Typography>
-            </Toolbar>
-          </AppBar>
+          <NavigationBar />
           
           <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
             <Routes>
               <Route path="/" element={<Dashboard />} />
               <Route path="/jobs" element={<JobList />} />
               <Route path="/jobs/:id" element={<JobDetail />} />
               <Route path="/analytics" element={<Analytics />} />
             </Routes>
           </Container>
         </Router>
       </ThemeProvider>
     </QueryClientProvider>
   );
 }

 export default App;