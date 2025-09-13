+import React, { Component, ErrorInfo, ReactNode } from 'react';
+import { Box, Typography, Button, Alert } from '@mui/material';
+import { Refresh } from '@mui/icons-material';
+
+interface Props {
+  children: ReactNode;
+}
+
+interface State {
+  hasError: boolean;
+  error?: Error;
+}
+
+class ErrorBoundary extends Component<Props, State> {
+  public state: State = {
+    hasError: false
+  };
+
+  public static getDerivedStateFromError(error: Error): State {
+    return { hasError: true, error };
+  }
+
+  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
+    console.error('Uncaught error:', error, errorInfo);
+  }
+
+  private handleReload = () => {
+    window.location.reload();
+  };
+
+  public render() {
+    if (this.state.hasError) {
+      return (
+        <Box 
+          display="flex" 
+          flexDirection="column" 
+          alignItems="center" 
+          justifyContent="center" 
+          minHeight="50vh"
+          p={4}
+        >
+          <Alert severity="error" sx={{ mb: 3, maxWidth: 600 }}>
+            <Typography variant="h6" gutterBottom>
+              Something went wrong
+            </Typography>
+            <Typography variant="body2" gutterBottom>
+              We're sorry, but something unexpected happened. Please try refreshing the page.
+            </Typography>
+            {process.env.NODE_ENV === 'development' && this.state.error && (
+              <Typography variant="caption" component="pre" sx={{ mt: 2, fontSize: '0.75rem' }}>
+                {this.state.error.message}
+              </Typography>
+            )}
+          </Alert>
+          
+          <Button
+            variant="contained"
+            startIcon={<Refresh />}
+            onClick={this.handleReload}
+          >
+            Refresh Page
+          </Button>
+        </Box>
+      );
+    }
+
+    return this.props.children;
+  }
+}
+
+export default ErrorBoundary;
+