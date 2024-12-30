import './App.css'
import { VscCheck, VscCopy, VscGithubInverted } from 'react-icons/vsc'
import { useEffect, useState } from 'react'
import { useCopyToClipboard } from 'react-use'

function App() {
  const [copied, setCopied] = useState<boolean>(true)
  const [state, copyToClipboard] = useCopyToClipboard()

  const cmd = 'docker run -d --name image ghcr.io/fuongz/image-proxy:v0.0.1'

  useEffect(() => {
    if (!state.error && state.value) {
      setCopied(true)
      setTimeout(() => {
        setCopied(false)
      }, 1000)
    } else {
      setCopied(false)
    }
  }, [state])

  return (
    <div className="flex mt-24 text-center antialiased justify-center items-center">
      <div className="container p-4 max-w-3xl">
        <h1 className="text-zinc-900 text-4xl mb-4 font-semibold">Image Proxy</h1>
        <p className="text-zinc-500 mb-6">A simple image converter API.</p>

        <a
          href="https://github.com/fuongz/image-proxy"
          target="_blank"
          className="group mb-8 mt-2 relative inline-flex h-10 items-center justify-center overflow-hidden rounded-md bg-neutral-950 px-6 font-medium text-neutral-200 transition hover:scale-110"
        >
          <span className="flex gap-4 items-center">
            <VscGithubInverted /> Source code
          </span>
          <div className="absolute inset-0 flex h-full w-full justify-center [transform:skew(-12deg)_translateX(-100%)] group-hover:duration-1000 group-hover:[transform:skew(-12deg)_translateX(100%)]">
            <div className="relative h-full w-8 bg-white/20"></div>
          </div>
        </a>

        <h3 className="font-semibold mb-2 text-lg">Run with Docker</h3>
        <div className="relative w-full border text-wrap font-medium border-zinc-200 px-4 py-2 rounded-md bg-zinc-50 pr-20">
          <pre>
            <code>{cmd}</code>
          </pre>

          <div
            onClick={() => copyToClipboard(cmd)}
            className="absolute right-1 cursor-pointer bg-white text-zinc-800 hover:transition hover:bg-zinc-100 transition top-1/2 -translate-y-1/2 transform border border-zinc-200 px-2 py-2 rounded-md"
          >
            {copied === false && <VscCopy />}
            {copied === true && <VscCheck />}
          </div>
        </div>

        <h3 className="font-semibold mb-2 text-lg mt-8">Usage</h3>
        <div className="relative break-words w-full border font-medium border-zinc-200 px-4 py-2 rounded-md bg-zinc-50 pr-20">
          <pre>
            <code className="break-words whitespace-pre">curl http://localhost/size(50,50)/IMG_URL</code>
          </pre>
        </div>

        <div className="text-zinc-600 mt-8">
          <p className="text-sm mt-0 mb-8 flex gap-1 justify-center items-center">
            Created by{' '}
            <a href="https://phuongphung.com/?ref=image-proxy" className="font-semibold underline" target="_blank">
              fuongz
            </a>
            .
          </p>
        </div>
      </div>
    </div>
  )
}

export default App
