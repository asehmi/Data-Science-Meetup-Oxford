const MyButton = (props) => {
  return (
    <button type="button" className="inline-flex items-center px-4 py-1 border border-transparent
                rounded-md shadow-sm text-md font-small text-white bg-indigo-600 hover:bg-pink-600
                focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                onClick={props.onClickHandler} disabled={props.props.disabled}>
          {props.label}
    </button>
  )
}

export default MyButton