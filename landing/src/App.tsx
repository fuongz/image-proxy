import "./App.css";

function App() {
  return (
    <div className="flex justify-center items-center h-screen">
      <div className="container prose">
        <h1 className="text-zinc-900">Image Proxy</h1>
        <p className="text-zinc-700">A simple image converter API.</p>

        <div className="relative">
          <div className="absolute top-0 leading-none rounded-tl-md rounded-br-md text-white font-semibold bg-green-600 py-2 px-4 left-0 text-sm">
            GET
          </div>
          <pre className="bg-green-50 border-green-200 border pt-10 text-green-800">
            <code>
              https://img.phake.app/format(
              <span className="text-red-500 italic">OUTPUT_FORMAT</span>
              ):size(<span className="text-yellow-500 italic">WIDTH</span>,
              <span className="text-yellow-500 italic">HEIGHT</span>)/
              <span className="text-blue-500 italic">IMAGE_URL</span>
            </code>
          </pre>
        </div>

        <ul>
          <li>
            <code>OUTPUT_FORMAT</code>: output image format (supported:{" "}
            <code>jpeg, png</code>)
          </li>
          <li>
            <code>WIDTH,HEIGHT</code>: resize image to be{" "}
            <code>WIDHT,HEIGHT</code> of width per size.
          </li>
          <li>
            <code>IMAGE_URL</code>: is the image URI. URI should be encoded by{" "}
            <code>
              <a
                className="font-semibold"
                href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent"
                target="_blank"
              >
                encodeURIComponent
              </a>
            </code>
          </li>
        </ul>

        <p>
          <span className="font-semibold">Demo:</span>{" "}
          <pre className="bg-zinc-200 text-zinc-900">
            <code>
              https://img.phake.app/size(500,500)/https://images.pexels.com/photos/27200179/pexels-photo-27200179/free-photo-of-landscape-of-hill-behind-flowers.jpeg
            </code>
          </pre>
        </p>

        <hr />
        <p className="text-sm">
          Check out the{" "}
          <a href="https://github.com/fuongz/image-proxy" target="_blank">
            source code
          </a>
          . Created by{" "}
          <a href="https://phuongphung.com/?ref=image-proxy" target="_blank">
            fuongz
          </a>
          .
        </p>
      </div>
    </div>
  );
}

export default App;
