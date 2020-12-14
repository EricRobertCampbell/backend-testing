export const add = (a, b) => {
	if (a === undefined || b === undefined) {
		return undefined;
	}
	if (typeof a !== "number" || typeof b !== "number") {
		throw new Error("You need to pass in a number!");
	}
	return a + b;
};

export const subtract = (a, b) => {
	return a - b;
};

export const multiply = (a, b) => {
	return a * b;
};

export const divide = (a, b) => {
	return a / b;
};
