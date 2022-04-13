import Control.Monad (forM_)
import Text.Printf (printf)
import Data.List (intercalate)

main :: IO ()
main = do
    t <- getLine
    forM_ [1..(read t :: Int)] $ \i -> do
        line <- getLine
        let r:c:_ = map read $ words line
        printf "Case #%d:\n" i
        putStrLn (solve r c)


solve :: Int -> Int -> String
solve r c = intercalate "\n" intermediate
    where intermediate :: [String] 
          intermediate = [[which i j | j <- [1..2*c+1]] | i <- [1..2*r+1]]
          which :: Int -> Int -> Char
          which 1 1 = '.'
          which 1 2 = '.'
          which 2 1 = '.'
          which 2 2 = '.'
          which i j 
            | i `mod` 2 == 1 = if j `mod` 2 == 1 then '+' else '-'
            | i `mod` 2 == 0 = if j `mod` 2 == 1 then '|' else '.'
