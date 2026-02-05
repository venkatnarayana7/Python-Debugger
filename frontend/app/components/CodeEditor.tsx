'use client';

import Editor from '@monaco-editor/react';

interface CodeEditorProps {
    value: string;
    onChange: (value: string) => void;
    language?: string;
    height?: string;
    readOnly?: boolean;
}

export default function CodeEditor({
    value,
    onChange,
    language = 'python',
    height = '400px',
    readOnly = false
}: CodeEditorProps) {
    return (
        <div className="border border-gray-700 rounded-lg overflow-hidden">
            <Editor
                height={height}
                language={language}
                theme="vs-dark"
                value={value}
                onChange={(val) => onChange(val || '')}
                options={{
                    minimap: { enabled: true },
                    fontSize: 14,
                    lineNumbers: 'on',
                    readOnly: readOnly,
                    automaticLayout: true,
                    scrollBeyondLastLine: false,
                    wordWrap: 'on',
                }}
            />
        </div>
    );
}
