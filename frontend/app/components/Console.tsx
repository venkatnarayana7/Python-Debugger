'use client';

import { useRef, useEffect } from 'react';
import { useEngineStore } from '@/lib/store';

export default function Console() {
    const logs = useEngineStore((state) => state.logs);
    const bottomRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom when new logs arrive
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [logs]);

    return (
        <div className="bg-gray-900 border border-gray-700 rounded-lg p-4 h-[300px] overflow-y-auto font-mono text-sm">
            <div className="text-gray-400 mb-2">$ Truth Engine Console</div>
            {logs.length === 0 ? (
                <div className="text-gray-500 italic">Waiting for execution...</div>
            ) : (
                logs.map((log, index) => (
                    <div
                        key={index}
                        className={`py-0.5 ${log.includes('[PASS]')
                                ? 'text-green-400'
                                : log.includes('[FAIL]') || log.includes('Error')
                                    ? 'text-red-400'
                                    : log.includes('...')
                                        ? 'text-yellow-400'
                                        : 'text-gray-300'
                            }`}
                    >
                        &gt; {log}
                    </div>
                ))
            )}
            <div ref={bottomRef} />
        </div>
    );
}
