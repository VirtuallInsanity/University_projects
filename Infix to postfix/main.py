import sys
from PyQt5 import QtWidgets
from form import Ui_MainWindow


class algapp(QtWidgets.QMainWindow):

    # initialization of the program when launch the app
    def __init__(self):
        super(algapp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

        self.inpt_inf_btn = ''
        self.output = ''
        self.step_var = False
        self.num_step = 0
        self.stack_array = []
        self.stack_step = ''

    # initiate ui logic
    def init_UI(self):
        self.setWindowTitle('LAB 1')
        self.ui.label_error.setHidden(True)

        self.ui.convertbutton.clicked.connect(self.converter)
        self.ui.clearbutton.clicked.connect(self.clear)
        self.ui.stepButton.clicked.connect(self.step)

        self.ui.plusButton.clicked.connect(lambda: self.button_input('+'))
        self.ui.minusButton.clicked.connect(lambda: self.button_input('-'))
        self.ui.expButton.clicked.connect(lambda: self.button_input('*'))
        self.ui.divButton.clicked.connect(lambda: self.button_input("/"))
        self.ui.powButton.clicked.connect(lambda: self.button_input('^'))
        self.ui.sqrtButton.clicked.connect(lambda: self.button_input('√'))
        self.ui.lnButton.clicked.connect(lambda: self.button_input('а'))
        self.ui.arcsinButton.clicked.connect(lambda: self.button_input('б'))
        self.ui.bracketLButton.clicked.connect(lambda: self.button_input('('))
        self.ui.bracketRButton.clicked.connect(lambda: self.button_input(')'))

        self.ui.pushButton_0.clicked.connect(lambda: self.button_input('j'))
        self.ui.pushButton_1.clicked.connect(lambda: self.button_input('a'))
        self.ui.pushButton_2.clicked.connect(lambda: self.button_input('b'))
        self.ui.pushButton_3.clicked.connect(lambda: self.button_input('c'))
        self.ui.pushButton_4.clicked.connect(lambda: self.button_input('d'))
        self.ui.pushButton_5.clicked.connect(lambda: self.button_input('e'))
        self.ui.pushButton_6.clicked.connect(lambda: self.button_input('f'))
        self.ui.pushButton_7.clicked.connect(lambda: self.button_input('g'))
        self.ui.pushButton_8.clicked.connect(lambda: self.button_input('h'))
        self.ui.pushButton_9.clicked.connect(lambda: self.button_input('i'))

    # implements button input
    def button_input(self, value):
        # lock certain button depends on the mode
        self.ui.stepMode.setEnabled(False)
        if self.ui.stepMode.isChecked():
            self.ui.convertbutton.setEnabled(False)
            self.ui.stepButton.setEnabled(True)
        else:
            self.ui.stepButton.setEnabled(False)

        # fill the infix input with buttons and convert input of some buttons to better visual format
        # self.ui.input_pre_f makes clicks display on the input line
        self.inpt_inf_btn += value
        if value == 'а':  # ru
            self.ui.input_pre_f.insert('ln')
            print(self.inpt_inf_btn)
            return None
        if value == 'б':  # ru
            self.ui.input_pre_f.insert('arcsin')
            print(self.inpt_inf_btn)
            return None
        self.ui.input_pre_f.insert(value)
        print(self.inpt_inf_btn)

    # clears variables, button settings and ui
    def clear(self):
        self.ui.label_error.setHidden(True)
        self.ui.convertbutton.setEnabled(True)
        self.ui.stepMode.setEnabled(True)
        self.ui.stepButton.setEnabled(True)
        self.ui.stepMode.setChecked(False)
        self.ui.input_pre_f.clear()
        self.ui.output_postf.clear()
        self.ui.label_combo.clear()
        self.ui.label_oper.clear()
        self.inpt_inf_btn = ''
        self.step_var = False
        self.num_step = 0
        self.output = ''
        self.stack_array = []
        self.stack_step = ''

    # implements step mode
    def step(self):
        self.step_var = True
        # calculate postfix form on the first step
        if self.num_step == 0:
            self.output = self.algorithm(self.inpt_inf_btn)
            self.ui.label_combo.clear()
        # untill input line not empty
        if len(self.inpt_inf_btn) != 0:
            # if there an operator check with the stack of operators
            if self.inpt_inf_btn[:1] == ''.join(self.stack_array[:1]):
                # if next element is + - ln or arcsin, add * or / to output
                if self.inpt_inf_btn[:1] in ['+', '-', 'а', 'б'] and self.output[self.num_step - 1] in ['*', '/']:
                    self.ui.label_oper.clear()
                    self.stack_step = self.stack_step[1:]
                    self.ui.output_postf.insert(self.stack_step)
                elif self.inpt_inf_btn[:1] in ['+', '-', 'а', 'б'] and self.output[self.num_step - 1] in ['+', '-',
                                                                                                           'а', 'б']:
                    self.ui.label_oper.clear()
                    self.stack_step = self.stack_step[1:]
                    self.ui.output_postf.insert(self.output[self.num_step - 1])

                self.stack_step += ''.join(self.stack_array[:1])
                self.ui.label_oper.setText(self.ui.label_oper.text() + '<p>%s</p>' % ''.join(self.stack_array[:1]))
                self.stack_array = self.stack_array[1:]
            else:
                self.ui.output_postf.insert(self.inpt_inf_btn[:1])

            self.num_step += 1
            self.inpt_inf_btn = self.inpt_inf_btn[1:]
            self.ui.input_pre_f.setText(self.inpt_inf_btn)
        else:
            self.ui.label_oper.clear()
            self.ui.output_postf.insert(
                self.stack_step[::-1])  # stack_step accumulate operators and prints them in label_oper
            self.ui.stepButton.setEnabled(False)

    # instant conversion
    def converter(self):
        postfix = self.algorithm(self.inpt_inf_btn)
        self.ui.output_postf.setText(postfix)
        self.ui.convertbutton.setEnabled(False)

    # method for locking buttons
    def error_button_lock(self):
        self.ui.label_error.setHidden(False)
        self.ui.convertbutton.setEnabled(False)
        self.ui.stepButton.setEnabled(False)
        return 'Error!'

    # calculate postfix form
    def algorithm(self, input):
        stack = []
        output = []

        # check for errors (iterate over all elements)
        for i in range(len(input) - 1):
            if input[i] in ['+', '-', '*', '/', '^', '√', '(', 'а', 'б'] and input[i + 1] in ['+', '-', '*', '/', '^',
                                                                                              ')']:
                return self.error_button_lock()
            if input[i - 1] not in ['+', '-', '*', '/', '^','√', 'а', 'б'] and input[i] in ['(']:
                return self.error_button_lock()
            if input[i] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'] and input[i + 1] in ['a', 'b', 'c', 'd',
                                                                                                   'e', 'f', 'g', 'h',
                                                                                                   'i', 'j']:
                return self.error_button_lock()

        for symbol in input:
            # operator
            if symbol in ['+', '-', '*', '/', '^', '√', '(', ')', 'а', 'б']:
                # handle '(' ')'
                if symbol == ')':
                    while stack[-1] != '(':
                        output.append(stack.pop())  # pop last element until '('
                    stack.pop()  # removing '('

                # implements logic of order of math operations
                if len(stack) != 0:
                    if stack[-1] in ['^', '√'] and symbol in ['+', '-', '*', '/', '^', '√']:
                        if stack[-1] in ['^', '√'] and symbol in ['^', '√']:
                            stack.append(symbol)
                            print(stack)
                            continue
                        output.append(stack.pop())
                        print(stack)

                    elif stack[-1] in ['*', '/'] and symbol in ['+', '-', '*', '/']:
                        output.append(stack.pop())
                        print(stack)

                    elif stack[-1] in ['+', '-', 'а', 'б'] and symbol in ['+', '-', 'а', 'б']:
                        output.append(stack.pop())
                        print(stack)

                # chane symbol from button to math operation for output
                if symbol == 'а':
                    symbol = 'ln'
                    stack.append(symbol) # add to stack ln instead of 'а' russian
                    # print nothing if set mode = True
                    if self.step_var:
                        pass
                    else:
                        self.ui.label_oper.setText(self.ui.label_oper.text() + '<p>%s</p>' % ''.join(symbol))
                    continue

                if symbol == 'б':
                    symbol = 'arcsin' # same for 'б'
                    stack.append(symbol)
                    # print nothing if set mode = True
                    if self.step_var:
                        pass
                    else:
                        self.ui.label_oper.setText(self.ui.label_oper.text() + '<p>%s</p>' % ''.join(symbol))
                    continue

                # not adding ')' to stack of operators
                if symbol == ')':
                    continue
                else:
                    stack.append(symbol)
                    # print nothing if set mode = True
                    if self.step_var:
                        pass
                    else:
                        self.ui.label_oper.setText(self.ui.label_oper.text() + '<p>%s</p>' % ''.join(symbol))
                    self.stack_array.append(''.join(symbol))
                print('stack: ' + ''.join(stack))
                print(self.stack_array)
            # operand
            else:
                self.ui.label_combo.setText(self.ui.label_combo.text() + '<p>%s</p>' % ''.join(output))
                output.append(symbol)
                print('Out: ' + ''.join(output))

        # add operators from end of stack to end of output
        while len(stack) != 0:
            output.append(stack.pop())

        # fill operators array
        self.stack_array.append(''.join(stack))
        print('stak: ' + ''.join(stack))
        print(self.stack_array)
        print('output: ' + ''.join(output))

        self.ui.label_combo.setText(self.ui.label_combo.text() + '<p>%s</p>' % ''.join(output))
        return ''.join(output)


# app initialization
app = QtWidgets.QApplication([])
application = algapp()
application.show()

sys.exit(app.exec())
