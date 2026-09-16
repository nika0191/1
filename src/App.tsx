import { Route, Routes } from "react-router-dom";

import ComponentsPage from "@/pages/components";
import IndexPage from "@/pages/index";

function App() {
  return (
    <Routes>
      <Route element={<IndexPage />} path="/" />
      <Route element={<ComponentsPage />} path="/components" />
    </Routes>
  );
}

export default App;
