'use client';

import { diffLines, Change } from 'diff';

interface DiffViewerProps {
    original: string;
    modified: string;
}

export default function DiffViewer({ original, modified }: DiffViewerProps) {
    const differences: Change[] = diffLines(original, modified);

    return (
        <div className="bg-gray-900 border border-gray-700 rounded-lg p-4 font-mono text-sm overflow-x-auto">
            <div className="text-gray-400 mb-3 font-sans font-semibold">
                Diff: Original → Fixed
            </div>
            <div className="space-y-0">
                {differences.map((part, index) => (
                    <div
                        key={index}
                        className={`py-0.5 px-2 ${part.added
                                ? 'bg-green-900/50 text-green-300 border-l-2 border-green-500'
                                : part.removed
                                    ? 'bg-red-900/50 text-red-300 border-l-2 border-red-500'
                                    : 'text-gray-400'
                            }`}
                    >
                        <pre className="whitespace-pre-wrap">
                            {part.added ? '+ ' : part.removed ? '- ' : '  '}
                            {part.value}
                        </pre>
                    </div>
                ))}
            </div>
        </div>
    );
}
