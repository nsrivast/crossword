#!/usr/bin/ruby
# model.rb
# builds clue-solving model data from corpus of real NYTimes xwords (.puz format)
# tags: ruby, crossword, acrosslite, puz, csv, date

# USAGE:
#
#   m1 = Model.new("nikhil", "all_puzzles.txt"); nil
#   m1.play_random(20, [6])
#
#   m2 = Model.new("james", "all_puzzles.txt"); nil
#   m2.play_existing("nikhil_results.txt")
#   m2.play_random(10, [4,5,6])
#

require 'acrosslite'
require 'date'
require 'pry'
require 'csv'
require 'iconv'

# === PROCESS CLUES ===

def write_clues_to_txt(puz_filenames, txt_filename)
  clues = []
  i_clue = 0
  puz_filenames.each do |puz_filename|
    puz_date = Date.strptime(File.basename(puz_filename)[0..-5], '%b%d%y')
    ac = Acrosslite.new(:filepath => puz_filename)
    (ac.down + ac.across).each do |x|
      clues << {:i => i_clue, :clue => x.clue, :answer => x.answer, :length => x.length, 
        :day_of_week => puz_date.wday, :year => puz_date.year, :fname => puz_filename}
      i_clue = i_clue + 1
    end
  end

  File.open(txt_filename, "w") do |f|
    clues.each{ |clue| f.puts clue.values.join("\t") }
  end
  return true
end

def load_clues_from_txt(txt_filename)
  ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
  clues = []
  File.open(txt_filename, 'r').readlines.each do |line|
    line = ic.iconv(line + ' ')[0..-2]
    vals = line.split("\t")
    clues << {:i => vals[0].to_i, :clue => vals[1], :answer => vals[2], :length => vals[3].to_i, 
      :day_of_week => vals[4].to_i, :year => vals[5].to_i, :fname => vals[6][0..-2]}
  end
  return clues
end

# === MODEL CLASS ===

class Model
  
  def initialize(player_name, clues_path)
    @player_name = player_name
    @clues = load_clues_from_txt(clues_path)
    @length_dict = build_length_dict(@clues)
    @daynames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return
  end

  def build_length_dict(clues)
    length_dict = {}
    clues.each do |clue|
      if length_dict.has_key?(clue[:length])
        length_dict[clue[:length]] = length_dict[clue[:length]] + [clue[:i]]
      else
        length_dict[clue[:length]] = [clue[:i]]
      end
    end
    return length_dict
  end

  # methods to play random or existing games
  
  def play_random(num_turns, word_lengths, filled=true)
    puts "Starting random play (" + num_turns.to_s + " turns, word lengths = " + 
      word_lengths.join(",").to_s + (filled ? ", partially filled" : "") + "). Press any key to start."
    gets
    results = []
    clues = num_turns.times.collect { @clues[ @length_dict[word_lengths.sample].sample ] }    
    clues.each do |clue|
      results << run_clue(clue, filled)
      puts "(n) next, (s) skip that one, (x) exit"
      resp = gets.chomp
      break if resp == "x"
      results = results[0..-2] if resp == "s"
    end
    save_results(results, "results/" + @player_name + Time.now.strftime("%Y%m%d_%H%M%S.txt"))
    return
  end
  
  def play_existing(load_path)
    puts "Starting existing play from " + load_path + ". Press any key to start."
    gets
    old_results = load_results(load_path)
    results = old_results.collect{ |clue| run_clue(clue) }
    save_results(results, "results/" + @player_name + Time.now.strftime("%Y%m%d_%H%M%S.txt"))
    return
  end
    
  # methods for single turn

  def run_clue(clue, filled=false)
    clue[:n_fills] ||= filled ? (1..(clue[:length]-1)).to_a.sample : 0
    clue[:prompt] ||= prompt(clue, filled)

    t1 = Time.now()
    puts "\n" + clue[:clue] + "\n" + clue[:prompt]
    clue[:guess] = gets.chomp.upcase
    t2 = Time.now()

    clue[:won] = (clue[:guess] == clue[:answer])
    puts response(clue)
    clue[:time] = t2 - t1
    clue[:player_name] = @player_name
    return clue
  end
  
  def prompt(clue, filled)
    prompt = ['_']*clue[:length]
    if filled
      to_fill = (0..(clue[:length]-1)).to_a.sort{ rand() - 0.5}[0..(clue[:n_fills]-1)]
      to_fill.each{ |i| prompt[i] = clue[:answer][i] }
    end
    return prompt.join(" ")
  end
  
  def response(clue)
    resp = "\n" + (clue[:won] ? "correct!" : "wrong, the answer was: " + clue[:answer] + ".") +
      " (" + @daynames[clue[:day_of_week]] + ", " + clue[:year].to_s + ")"
    return resp
  end
  
  # results i/o
  
  def save_results(results, save_path)
    File.open(save_path, "w") do |f|
      results.each{ |result| f.puts result.values.join("\t") }
    end
  end

  def load_results(load_path)
    ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
    results = []
    File.open(load_path, 'r').readlines.each do |line|
      line = ic.iconv(line + ' ')[0..-2]
      vals = line.split("\t")
      results << {:i => vals[0].to_i, :clue => vals[1], :answer => vals[2], :length => vals[3].to_i, 
        :day_of_week => vals[4].to_i, :year => vals[5].to_i, :fname => vals[6],
        :n_fills => vals[7].to_i, :prompt => vals[8], :guess => vals[9], :won => vals[10], :time => vals[11].to_f,
        :player_name => vals[12][0..-2]}
    end
    return results
  end
end
