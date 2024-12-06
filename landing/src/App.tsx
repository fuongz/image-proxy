import './App.css'
import { VscCopy, VscGithubInverted, VscPlay } from 'react-icons/vsc'
import { useEffect, useMemo, useState } from 'react'
import { useCopyToClipboard } from 'react-use'

const PROXY_URL: string = 'https://img.phake.app/'

function App() {
  const [copied, setCopied] = useState<boolean>(true)
  const [testUrl, setTestUrl] = useState<null | string>(null)
  const [imageState, setImageState] = useState<string>('idle')
  const [state, copyToClipboard] = useCopyToClipboard()
  const [format, setFormat] = useState<string>('png')
  const [imageUrl, setImageUrl] = useState<string>('https://images.pexels.com/photos/27200179/pexels-photo-27200179/free-photo-of-landscape-of-hill-behind-flowers.jpeg')
  const [resizeWidth, setResizeWidth] = useState<number | string>(200)
  const [resizeHeight, setResizeHeight] = useState<number | string>(200)
  const [quality, setQuality] = useState<string | number>(70)

  const [error, setError] = useState<string | null>(null)
  const [options, setOptions] = useState<{ [key: string]: string | number }>({
    format,
    size: `${resizeWidth}, ${resizeHeight}`,
    quality,
  })

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

  const result = useMemo(() => {
    return `${PROXY_URL}${
      Object.keys(options).length > 0
        ? Object.keys(options)
            .filter((key) => options[key])
            .map((key) => `${key}(${options[key]})`)
            .join(':')
        : 'default'
    }/${imageUrl}`
  }, [options])

  const handleSubmit = () => {
    if (!imageUrl) {
      setError('Please fill the image url')
      return
    } else {
      setError(null)
    }

    const newOptions = {
      format: options.format,
      quality: options.quality,
      size: options.size,
    }

    newOptions.format = format
    newOptions.size = `${resizeWidth},${resizeHeight}`
    newOptions.quality = quality

    setOptions(newOptions)
  }

  const handleShowTestImage = () => {
    if (result !== testUrl) {
      setTestUrl(result)
      setImageState('loading')
    }
  }

  const handleOnLoadImage = () => {
    setImageState('loaded')
  }

  return (
    <div className="flex mt-24 antialiased justify-center items-center">
      <div className="container p-4 max-w-lg">
        <h1 className="text-zinc-900 text-4xl mb-4 font-medium">Image Proxy</h1>
        <p className="text-zinc-500 mb-6">A simple image converter API.</p>

        <div className="relative flex gap-4">
          <input type="text" value={imageUrl} onChange={(e) => setImageUrl(e.target.value)} className="w-full border px-4 py-2 rounded-xl border-zinc-200" placeholder="Enter image url" />
        </div>

        <div className="relative mt-4 flex gap-4 whitespace-nowrap flex-wrap text-sm">
          <div className="relative flex gap-2 items-center">
            <label htmlFor="format">
              Image <b>format</b>
            </label>
            <select
              className="border border-zinc-200 px-2 py-1 rounded"
              name="format"
              id="format"
              value={format}
              onChange={(e) => {
                setFormat(e.target.value)
              }}
            >
              <option value="png">.PNG</option>
              <option value="jpeg">.JPEG</option>
              <option value="webp">.WEBP</option>
            </select>
          </div>
          <div className="relative flex gap-2 items-center">
            <label htmlFor="resizeWidth">
              and resize to <b>width</b> ={' '}
            </label>
            <input
              className="border w-24 border-zinc-200 px-2 py-1 rounded"
              name="resizeWidth"
              id="resizeWidth"
              type="number"
              value={resizeWidth}
              onChange={(e) => {
                setResizeWidth(e.target.value)
              }}
              placeholder="width"
            />
            x <b>height</b>=
            <input
              className="border w-24 border-zinc-200 px-2 py-1 rounded"
              name="resizeHeight"
              id="resizeHeight"
              value={resizeHeight}
              onChange={(e) => {
                setResizeHeight(e.target.value)
              }}
              type="number"
              placeholder="height"
            />
          </div>
          {format === 'webp' && (
            <div className="relative flex gap-2 items-center">
              <label htmlFor="resizeWidth">
                and image <b>quality</b> will optimize to
              </label>
              <input
                className="border w-24 border-zinc-200 px-2 py-1 rounded"
                name="resizeWidth"
                id="resizeWidth"
                type="number"
                placeholder="75"
                value={quality}
                onChange={(e) => {
                  setQuality(e.target.value)
                }}
              />{' '}
              %
            </div>
          )}
        </div>

        <div className="mt-8">
          <button
            onClick={() => {
              handleSubmit()
            }}
            className="cursor-pointer rounded-lg bg-neutral-900 px-4 font-semibold py-2 text-sm text-neutral-100 transition-colors hover:bg-neutral-700 active:bg-neutral-800"
          >
            Try it out
          </button>
        </div>

        {!!options && (
          <>
            <div className="flex justify-between items-center mt-4">
              <div className="font-semibold mt-4">RESULT:</div>
              <div
                onClick={() => copyToClipboard(result)}
                className="rounded-lg text-sm flex gap-1 hover:bg-neutral-600 transition hover:transition text-white bg-neutral-700 items-center top-2 py-1 right-4 cursor-pointer px-3"
              >
                <VscCopy /> {copied ? 'Copied!' : 'Copy'}
              </div>
            </div>
            <div className="mt-2 w-full px-4 pt-2 pb-2 text-balance break-words rounded bg-blue-50 border border-blue-200 text-zinc-400 relative">
              {PROXY_URL}
              {Object.keys(options).length > 0
                ? Object.keys(options)
                    .filter((key) => options[key])
                    .map((key, index: number) => (
                      <span key={`option-${key}`}>
                        {index === 0 ? '' : ':'}
                        <span className="text-orange-600">
                          {key}(<span className="font-semibold">{options[key].toString().trim()}</span>)
                        </span>
                      </span>
                    ))
                : 'default'}
              /<span className="text-blue-600">{imageUrl}</span>
            </div>

            <div className="relative mt-4">
              <div>
                <button
                  disabled={imageState === 'loading'}
                  onClick={() => handleShowTestImage()}
                  className="disabled:cursor-not-allowed mb-4 disabled:hover:bg-white disabled:border-blue-300 disabled:hover:text-blue-300 disabled:text-blue-300 border-blue-600 text-sm inline-flex gap-4 items-center font-medium text-blue-600 border shrink-0 rounded px-4 py-2 hover:bg-blue-600 hover:text-white  transition  hover:transition"
                >
                  <VscPlay /> {imageState === 'loading' ? 'Loading...' : 'Preview'}
                </button>
              </div>

              {!!testUrl && (
                <div className="mb-6">
                  <span className="mt-4 block text-sm font-semibold">CODE:</span>
                  <pre className="bg-blue-50 mb-4 px-4 py-2 rounded-lg whitespace-break-spaces break-words mt-2 border-blue-200 border text-blue-600">
                    <code>{`<img src="${testUrl}" />`.toString()}</code>
                  </pre>
                  <img onLoad={handleOnLoadImage} className={`${imageState !== 'loaded' ? 'hidden' : ''}`} src={testUrl} alt="" />

                  {imageState !== 'loaded' && (
                    <div className="flex animate-pulse flex-wrap items-center gap-8">
                      <div className="grid h-56 w-56 place-items-center rounded-lg bg-gray-200">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1} stroke="currentColor" className="h-12 w-12 text-gray-300">
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H3.75A1.5 1.5 0 0 0 2.25 6v12a1.5 1.5 0 0 0 1.5 1.5Zm10.5-11.25h.008v.008h-.008V8.25Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z"
                          />
                        </svg>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </>
        )}

        {!!error && <div className="mt-4 px-4 rounded py-2 text-sm bg-red-50 border border-red-200 text-red-500">{error}</div>}

        <hr />
        <p className="mb-0 mt-4 text-center">
          <a className="inline-flex gap-1 items-center" href="https://status.phake.app/?utm_source=status_badge" target="_blank">
            <img src="https://uptime.betterstack.com/status-badges/v3/monitor/1oiyb.svg" alt="image proxy's status page" />
          </a>
        </p>
        <p className="text-sm mt-0 mb-8 flex gap-1 justify-center items-center">
          <a className="inline-flex gap-1 items-center" href="https://github.com/fuongz/image-proxy" target="_blank">
            <VscGithubInverted /> Source code
          </a>
          | Created by{' '}
          <a href="https://phuongphung.com/?ref=image-proxy" target="_blank">
            fuongz
          </a>
          .
        </p>
      </div>
    </div>
  )
}

export default App
