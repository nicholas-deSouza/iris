import '@blocknote/core/fonts/inter.css';
import '@blocknote/mantine/style.css';
import { useCreateBlockNote } from '@blocknote/react';
import { BlockNoteView } from '@blocknote/mantine';
import './App.css';

function App() {
  const editor = useCreateBlockNote();

  return (
    <div className="editor-page">
      <BlockNoteView editor={editor} />
    </div>
  );
}

export default App;
