(* $Id: Genetic.m,v 1.0 1996/06/30 23:48:28 rory Exp $ *)
(*: Version: Mathematica 2.2 *)
(*: Name: Genetic' *)
(*: Title: Genetic Programming *)
(*: Author: Gregory M. Matous *)
(*: Keywords: Genetic, Programming, Evolve, fitness *)
(*: Requirements: none. *)
(*: Warnings: Does limited error handling. *)
(*: Sources: *)
(*: Summary: This package creates a population of cells, each with its own genetic -code-. Each cell is an object. *)

BeginPackage["Genetic`", "Classes`"];

Cell::usage = "Cell [index] references a cell object. CellFitness and CellShow are methods of the cell object."
CellObject::usage = "CellObject references the class."
CellCreate::usage = "CellCreate [input, test] declares a class, named -CellObject-, with a fitness test which applies input to the gene."
PopCreate::usage = "CreatePop [functions, arguments, popsize] creates indexed instances of the class Cell with a random genetic structure as an instance variable."
PopUpdate::usage = "PopUpdate [options] generates a new population of cells based on the old population, wherein cells in the old population combine by crossover. Options include Selection-> {Rank, Proportionate, Tournament), Tournament Size, MaximumDepth, Crossover Proportion."

(* == 1 == *)

CellFitness::usage = "CellFitness is a method of CellObject."
CellShow::usage = "CellShow is a method of CellObject."
CellPlot::usage = "CellPlot [expr] generates a graphical representation of an expression, viewed as a tree."
PopBin::usage = "PopBin[index, bina] groups the population into bins."
MaxFitness::usage = "Cell with maximum fitness"
MinFitness::usage = "Cell with minimum fitness."
PopUpdate::option = "Option ('1') is not allowed."

Options[PopUpdate] = {TournamentSize :> PopSize / 10, Selection -> Rank, CrossoverProportion -> 9 / 10, MaximumDepth -> 20}; {Proportionate, Tournament, PopSize);
(* Minfit, Maxfit, PopSize are non-local vars. *)
Begin["`Private`"];

(* ************ CellCreate ********* *)

CellCreate[input_, test_] :=
    Class[ CellObject, Object,
      {gene, fit},
      {
        {new, (new[super]; gene = #1; fit = test[input, gene])&}, {CellFitness, 1 / (1 + fit) &}, (* Adjusted fitness *)
        {CellShow, gene&},
        {fission, (Part[ Position[gene, _, Heads -> False], Random[Integer, {1, leafCount[gene]}] ] ) &}
      }
    ];

(* ******** PopCreate ************* *)

PopCreate[functions, arguments, popsize_ : 100] := (
  CellFitness[n_Integer] := CellFitness[ Cell[n]];
  CellShow[n_Integer] := CellShow[ Cell[n]];

  (* == 2 == *)

  PopSize = popsize;
  babies = Map[# /. (f_[x__] :> f @@ Array[t&, Length[{x}]] )&, functions];
  Default[randomBaby] = Identity;
  randomBaby[_.] := Part[babies, Random[Integer, {1, Length[babies]}] ];
  randomPart[stuff List] := Part[stuff, Random[Integer, {1, Length[stuff]}] ];
  leafReplacer[_] :=
      If[( (Random[] < counter / PopSize) || EvenQ[counter]),
        randomBaby[], randomPart[arguments]]; (* 50% ramp prob *)
  Evaluate[ Array[Cell, PopSize]] = Map[new[CellObject, #] &,
    Table[
      Nest[
        (Map[ leafReplacer, #, {Depth[#] - 1}])&,
        randomBaby[], Ceiling[counter + 6 / PopSize] (* depth of Nesting varies *) ] (* from 1 to 6 *)
          /. t :> randomPart[arguments], (* sub. randomly from args *)
      {counter, PopSize}]
  ]
)

    (* ********* selectParent ****** *)

    selectParent[] := Module[{prop, rand},
  Switch[
    Selection /. Options[PopUpdate],
    Proportionate,
    prob = Random[Real, {CellFitness[Minfit], CellFitness[Maxfit]}];
    rand = Random[Integer, {1, PopSize}];
    While[
      CellFitness[rand] < prob,
      rand - Random[Integer, {1, PopSize}]];
    rand,
    Rank,
    Part[PopSort[], Ceiling[PopSize * (1 - Sqrt[1 - Random[]])] ],
    Tournament,

    (* == 3 == *)

    MaxFitness[ Take[ RandomPermutation[PopSize], TournamentSize /. Options[PopUpdate]]]
  ]]


    (* ******* Crossover ******** *)

    Crossover[] :=
    Module[{indx1, indx2, fissi, fiss2, gene1, gene2,
      maxdepth = MaximumDepth /. Options[PopUpdate]},
      {indx1, indx2} = { selectParent[], selectParent[] };
      {fissi, fiss2} = {fission[ Cell[indx1]], fission[ Cell[indx2]] }; Print["fissions=", fissi, "and", fiss2, "indx 1&2=", indx1, "and", indx2]; {gene1, gene2} = { ReplacePart[ CellShow[indx1],
        Part[ CellShow[indx2], Sequence @@ fiss2], fiss1], ReplacePart[ CellShow[indx2],
        Part[ CellShow[indx1], Sequence @@ fiss1], fiss2] };
      If[ (Depth[gene1] > maxdepth || Depth[gene2] > maxdepth), Crossover[], {gene1, gene2} ]
    ]

        (* ****** PopUpdate ****** *)

        PopUpdate[opts___Rule] := Module[{crossprop}, If[ MemberQ[{Proportionate, Rank, Tournament}, Selection /. {opts} /. Options[PopUpdate]], SetOptions[PopUpdate, opts],
      Return[ Message[PopUpdate::option, opts]]
    ];
    crossprop = Crossover Proportion /. Options[PopUpdate];
    Evaluate Array[Cell, PopSize]] = Map[new[CellObject, #] &, Flatten[ Table[
      If[
        counter <= Floor[crossprop / 2 PopSize],
        Crossover[], CellShow[selectParent[]]
      ],
      {counter, PopSize - Floor[crossprop / 2 PopSize]}]]
    ];
PopSort[] = PopSort[ Range[PopSize]];
Minfit = First[ PopSort[] ]; Maxfit = Last[ PopSort[] ];
]

(* ******* PopSort, PopBin *********** *)

(* == 4 == *)

PopSort[index List] := Sort[ index, CellFitness[#2] > CellFitness[#1]&]
    PopBin[index List, bins Integer : Positive] : Block[
  {delta (Maxfit - Minfit) / bins},
  Table[
    Select[index, (CellFitness[#] >= i && CellFitness[#] <= i + delta)&], {i, Minfit, Maxfit - delta, delta}
  ]]

    RandomPermutation[n_Integer?Positive] :=
    Block[(t),
      Array[{Random[], #} &, n];
      t = Sort[t];
      Map[ #[[2]] &, t ]
    ]

        (* ****** CellPlot ** ******* *)

        $TreeWidth = 2.1
        $TreeHeight = 0.8
        CellPlot[expr_Integer] := Show[Graphics[CellPloto[ CellShow[expr],
      0, 0, 1], PlotRange -> All]];

CellPlot[expr_] := Show[Graphics[CellPloto[expr, 0, 0, 11, PlotRange -> All]];

CellPlot0[f_[children__], x, y, n_] :=
    Block[{xl, xr, c, xi, gnew, gthis, i, dx},
      c = {children};

      If[Length[c] == 1,
        Return[
          Flatten[
            { Line[{{x, y}, {x, y + 1}}],
              Text[f, {x, y}],
              Text[ If[AtomQ[Sequence @@ c],
                Sequence @@ c, Head[Sequence @@ c]], {x, y + 1}],
              CellPlot0[First[c], x, y + 1, 1]}
          ]]];

      x1 = x - $TreeWidth ^(-y) 2 / n;
      xr = x + $TreeWidth ^(-y) 2 / n;

      dx = N[(xr - x1) / (Length[c] - 1)] ;
      gnew = Table[ If[! AtomQ[c[[i + 1]]],
        CellPlotO[c[[i + 1]], x1 + i dx, y + 1, Length[c]].
            {} ],
        {i, 0, Length[c] - 1} ];

      (* == 5 == *)

      gthis = Table[xi = xl + i dx ;
      { Line[{{xi, y}, {xi, y + 1}}],
        Text[ If[ AtomQ[ c[[i + 1]] ], c[[i + l]], ""], {xi, y + 1}] },
        {i, 0, Length[c] - 1}]
          // Append[#, Text[f, {(x1 + (Length[c] - 1) * dx / 2), y}] ]& ;
      Flatten[{Line[{{xl, y}, {xr, y}}], gthis, gnew}]
    ]
        CellPlot0[e_, x, y_, n_] := {};
End[]
    EndPackage[]


