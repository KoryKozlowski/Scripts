;Author: Kory Kozlowski
;CSE 3341 Project 2
;-------------------------------------------
;Description: an interpreter for the PLAN
;programming language, written in scheme. 
;-------------------------------------------
;Legal built-in scheme functions:
;  equal?, car, cdr, cons, cond, if, +, *, 
;  null?, symbol?, integer?
;-------------PLAN-GRAMMAR------------------
;<Program> ::= ( prog <Expr> )
;<Expr> ::= <Id>  |
;           <Const> |
;          ( myignore  <Expr> ) |
;          ( myadd  <Expr>  <Expr> )  |
;          ( mymul  <Expr>  <Expr> ) |
;          ( myneg  <Expr> ) | 
;          ( mylet  <Id> <Expr> <Expr> )
;<Id> ::= a | b | ... | z
;<Const> ::= integer constant
;-------------------------------------------

;builds list of PLAN program values 
(define (MyInterpreter list)
  ;if list = empty (end of prog list)
  ;then, return empty list
  (cond((null? list) list)
  ;otherwise, evaluate first prog
  ;then, recursively evaluate next prog
  (else
   (cons(EvalExpr (car list) '()) (MyInterpreter(cdr list))))))

;-------------------------------------------

;idTable organization: {(id,const),(id,const),...}
;cdr(idPair) = idValue, car(idPair) = id
(define (idTable ids symbol)
  ;if idTable = empty, return empty list
  (cond ((null? ids) '())
       ;if symbol = current id, return value
       ((equal? symbol (car(car ids)))(cdr(car ids)))
       ;otherwise, move to next id in table
       (else
        (idTable (cdr ids) symbol))))

;-------------------------------------------

;check first element in given expr 
;if keyword, evaluate accordingling
;if id, lookup in idTable and return value
;if integer, return value
(define (EvalExpr expr ids)
  ;if integer, return value
  (cond ((integer? expr) expr)
	;if id, lookup idValue in idTable
	((symbol? expr) (idTable ids expr))
  	;if prog, evaluate inner expression
	((equal? (car expr) 'prog)
		;if int after prog, return value (prog ended)
		(cond ((integer? (car(cdr expr)))(car(cdr expr)))
		(else (EvalExpr (car(cdr expr)) ids))))
    ;if myignore, expr = 0
    ((equal? (car expr) 'myignore) 0)
    ;if myadd, (expr1)+(expr2)
    ((equal? (car expr) 'myadd)
        (+(EvalExpr (car(cdr expr)) ids) 
			(EvalExpr (car(cdr(cdr expr))) ids)))
    ;if mymul, (expr1)*(expr2)
    ((equal? (car expr) 'mymul)
        (*(EvalExpr (car(cdr expr)) ids) 
            (EvalExpr (car(cdr(cdr expr))) ids)))
    ;if myneg, expr = (-1(expr))
    ((equal? (car expr) 'myneg)
        (* -1(EvalExpr (car(cdr expr)) ids)))
    ;if mylet...
    ((equal? (car expr) 'mylet)
	;eval. 2nd expression
	(EvalExpr (car(cdr(cdr(cdr expr))))
		;eval. 1st expression and then 
		;cons with the id (make tuple)
        	(cons (cons (car(cdr expr)) 
			(EvalExpr (car(cdr(cdr expr))) 
				ids)) ids)))))