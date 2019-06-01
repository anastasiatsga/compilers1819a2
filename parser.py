"""
	Grammar
	-------
	Stmt_list   -> Stmt Stmt_list | .
	Stmt        -> id assign Expr | print Expr.
	Expr        -> Term Term_tail.
	Term_tail   -> xor Term Term_tail | .
	Term        -> Factor Factor_tail.
	Factor_tail -> or Factor Factor_tail | .
	Factor      -> Atom Atom_tail.
	Atom_tail   -> and Atom Atom_tail | .
	Atom        -> leftPar Expr rightPar | id | number.
	FIRST sets
	----------
	Stmt_list:		id print
	Stmt:			id print
	Term_tail:		xor
	Term:			leftPar id number
	Factor_tail:	        or
	Factor:			leftPar id number
	Atom_tail:		and
	Atom:			leftPar id number
	Expr:			leftPar id number
	FOLLOW sets
	-----------
	Stmt_list:		∅
	Stmt:			id print
	Term_tail:		rightPar id print
	Term:			rightPar xor id print
	Factor_tail:	        rightPar xor id print
	Factor:			rightPar or xor id print
	Atom_tail:		rightPar or xor id print
	Atom:			rightPar and or xor id print
	Expr:			rightPar id print
	"""

	
	



	import plex




	class ParseError(Exception):
	    pass




	class MyParser:
	   	   
	    def create_scanner(self, fp):
	        
	       
	        and_operator = plex.Str('and')
	        or_operator = plex.Str('or')
	        xor_operator = plex.Str('xor')
	        assignment_operator = plex.Str('=')
	        print_operator = plex.Str('print')


	        space = plex.Any(' \t\n')
	        parenthesis_opened = plex.Str('(')
	        parenthesis_closed = plex.Str(')')
	        binary = plex.Rep1(plex.Range('01'))
	        digit = plex.Range('09')
	        letter = plex.Range('AZaz')        
	        variable = letter + plex.Rep(letter|digit)


	      
	        lexicon = plex.Lexicon([
	            (and_operator, 'and'),
	            (or_operator, 'or'),
	            (xor_operator, 'xor'),
	            (assignment_operator, '='),
	            (print_operator, 'print'),            
	            (space, plex.IGNORE),
	            (parenthesis_opened, '('),
	            (parenthesis_closed, ')'),
	            (binary, 'bin'),
	            (variable, 'var')            
	            ])


	       	        self.scanner = plex.Scanner(lexicon, fp)
	        self.la, self.val = self.next_token()




	    def next_token(self):
	       
	        return self.scanner.read()


	    def position(self):
	       	        return self.scanner.position()


	    def match(self, token):
	        
	        if self.la == token:
	            self.la, self.val = self.next_token()
	        else:
	            raise ParseError('found {} instead of {}'.format(self.la, token))


	    def parse(self, fp):
	    
	        self.create_scanner(fp)
	        self.stmt_list()


	    def stmt_list(self):
	        	        if self.la == 'var' or self.la == 'print':
	            self.stmt()
	            self.stmt_list()
	            return
	        elif self.la is None:
	            return
	        else:
	            raise ParseError('in stmt_list: "var" or "print" expected')
	        
	    def stmt(self):
	      
	        if self.la == 'var':
	            self.match('var')
	            self.match('=')
	            self.expr()
	            return
	        elif self.la == 'print':
	            self.match('print')
	            self.expr()
	            return
	        else:
	            raise ParseError('in stmt: "var" or "print" expected')


	    def expr(self):
	      	        if self.la == '(' or self.la == 'var' or self.la == 'bin':
	            self.term()
	            self.term_tail()
	            return
	        else:
	            raise ParseError('in expr: "(", "var" or "bin" expected')


	    def term_tail(self):
	      
	        if self.la == 'xor':
	            self.match('xor')
	            self.term()
	            self.term_tail()
	            return
	        elif (self.la == ')' or self.la == 'var' or
	                self.la == 'print' or self.la is None):     	            return
	        else:
	            raise ParseError('in term_tail: "xor", ")", '
	                             + '"var" or "print" expected')


	    def term(self):
	        
	        if self.la == '(' or self.la == 'var' or self.la == 'bin':
	            self.factor()
	            self.factor_tail()
	            return
	        else:
	            raise ParseError('in term: "(", "var" or "bin" expected')


	    def factor_tail(self):
	      
	        if self.la == 'or':
	            self.match('or')
	            self.factor()
	            self.factor_tail()
	            return
	        elif (self.la == ')' or self.la == 'xor' or self.la == 'var'
	                or self.la == 'print' or self.la is None):  
	            return
	        else:
	            raise ParseError('in term_tail: "or", ")", "xor", '
	                             + '"var" or "print" expected')


	    def factor(self):
	        	        if self.la == '(' or self.la == 'var' or self.la == 'bin':
	            self.atom()
	            self.atom_tail()
	            return
	        else:
	            raise ParseError('in factor: "(", "var" or "bin" expected')


	    def atom_tail(self):
	       
	        if self.la == 'and':
	            self.match('and')
	            self.atom()
	            self.atom_tail()
	            return
	        elif (self.la == ')' or self.la == 'or' or self.la == 'xor'
	                or self.la == 'var' or self.la == 'print'
	                or self.la is None):                    	            return
	        else:
	            raise ParseError('in atom_tail: "and", ")", "or", "xor", '
	                             + '"var" or "print" expected')


	    def atom(self):
	        
	        if self.la == '(':
	            self.match('(')
	            self.expr()
	            self.match(')')
	            return
	        elif self.la == 'var':
	            self.match('id')
	            return
	        elif self.la == 'bin':
	            self.match('bin')
	            return
	        else:
	            raise ParseError('in atom: "(", "var" or "bin" expected')




	# The main part of program
	parser = MyParser()
	with open("binfile.txt", "r") as fp:
		try:
			parser.parse(fp)
		except plex.errors.PlexError:
			_, lineno, charno = parser.position()	
			print("Scanner Error: at line {} char {}".format(lineno, charno+1))
		except ParseError as perr:
			_, lineno, charno = parser.position()	
			print("Parser Error: {} at line {} char {}"\
	              .format(perr, lineno, charno+1))
