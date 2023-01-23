console.log("scientific calculator");


const actions = document.querySelector('.actions');
const header = document.querySelector('.header');
// input field
// accessing the user input field value
const ans = document.querySelector('.input_field');
console.log(actions);
let mplus = [0];
let mminus = [0];
let final_output = 0;
// use the let for assigning the value to expression
let expression = '';
let a=0;
actions.addEventListener('click', (e) => {
	console.log(e.target);
	const value = e.target.dataset['value'];
	console.log("values",value)

	// value must be enter, if value is undefined noting is happen
	if(value !== undefined) {
		
		// clear all the input value
		if(value == 'clear') {
			expression = '';
			ans.value = 0;
			return true;
		}
		// remove the one number at a time using slice() method
		else if(value == 'delete'){
			let remove = ans.value.slice(0, -1);
			console.log(remove);
			expression = remove;
		}
		else if(value == 'square'){
			expression = square();
		}
		else if (value == '1/x'){
			expression = reciprocalfn();
		}
		else if (value == 'π'){
			expression = 3.14159
		}
		else if(value == 'm+'){
			mplus[0] += expression;
			console.log(mplus[0]);
		}
		else if (value == 'm-'){
			mminus[0] += expression;
			console.log(mminus[0]);
		}
		else if(value == 'ms'){
			final_output = mplus[0] - mminus[0];
			expression = '';
			ans.value = 0;
			alretfunction(final_output);
			// display the message final output are stored in memory
			console.log(final_output);
		}
		else if(value == 'mc'){
			mplus = [0]
			mminus = [0]
			final_output = 0;
			expression = '';
			ans.value = 0;
		}
		else if(value == 'mr'){
			expression = final_output;
		}
		else if(value == 'log'){
			let ans = Math.log10(expression);

			console.log("ans", ans);
			expression = ans;
		}
		// calculating the factorial number
		else if(value == '!'){
			expression = fact(expression);
		}
		else if(value == 'deg'){
			expression = expression * (Math.PI/180);
		}
		else if(value == 'euler_number'){
			expression = '2.718281828459045';
			console.log("expression", expression);
		}
		else if(value == 'abs'){
			expression = Math.abs(eval(expression));
			
		}
		// exponential function
		else if(value == 'exp'){
			// let e = '2.718281828459045';
			expression = Math.exp(expression);
		}
		// sqrt function
		else if(value == 'sqrt'){
			expression = Math.sqrt(expression);
		}
		else if(value == '10squarex'){
			expression = 10 ** expression
		}
		// x ** y operation
		else if(value == 'xsquarey'){
			expression += "**";
		}
		else if(value == 'natural_logarithm'){
			expression = Math.log(expression)
		}
		else if(value == 'fe'){
			expression = parseFloat(expression).toExponential(2);
		}
		else if(value == 'plus&minus'){
			if (expression[0] == '+'){
				console.log("plus");
				expression = '-' + expression.slice(1)	;
			}
			else{
				expression = '+' + expression.slice(1)	;
			}
		}

		// trigonometry operation

		// sin operation
		else if(value == 'sin'){
			expression = Math.sin(expression  * (Math.PI/180));
		}
		// con operation
		else if(value == 'cos'){
			expression = Math.cos(expression * (Math.PI/180));
		}
		// tan operation
		else if(value == 'tan'){
			expression = Math.tan(expression * (Math.PI/180));

		}
		// sec operation
		else if(value == 'sec'){
			expression = 1/(Math.cos(expression * (Math.PI/180)));
		}
		// cosec operation
		else if(value == 'cosec'){
			expression = 1/(Math.sin(expression * (Math.PI/180)));
		}

		// cot operation
		else if(value == 'cot'){
			expression = 1/(Math.tan(expression * (Math.PI/180)));
		}
		// else if (value == 'm+'){
		// 	var mm1 = mm1 + expression;
		// 	localStorage.setItem(value, mm1);
		// 	console.log(localStorage);
		// }
		// else if (value == 'm-'){
		// 	var mm2 = mm2 - expression;
		// 	localStorage.setItem(value, mm2);
		// 	console.log(localStorage);
		// }
		else if(value == '=') {
			const answer = eval(expression);
			expression = answer;
			
		} else {
			expression += value;
		}

		if(expression == undefined) {
			expression = '';
			ans.value = 0;
		} else {
			ans.value = expression;
		}
		// expression += value;
	}

});

// function for square operation
const square =()=> {
	return eval(expression*expression);
}

// function for reciprocal function operation
const reciprocalfn = () => {
	return eval(1/expression)
}

// calculating the factorial number
const fact = (expression) => {
	if(expression < 0){
		return 0;
	}
	else if (expression === 1){
		return 1;
	}
	else{
		let fact_no = 1;
		for (i=1; i<=expression; i++){
			fact_no *= i;
		}
		return fact_no;
	}
}

// const xsquarey = () => {
// 	expression += '**';

// }


const alretfunction = (final_output) => {

	if (final_output != 0){
	header.setAttribute("style", "margin-left: 490px;background-color: rgb(241 243 244);padding: 30px;width: 23%;");
    

	header.innerHTML = 'Output Are Stored in memory';
	setTimeout(function () {
	    // Closing the alert
	        $('#alert').alert('close');
	    }, 5000);
	}
}


